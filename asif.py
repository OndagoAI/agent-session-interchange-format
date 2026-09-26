#!/usr/bin/env python3
"""Local, vendor-neutral ASIF reference commands. No agent execution or network access."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
from jsonschema.exceptions import ValidationError, SchemaError
from reference.common import load, read, encode, Invalid, Unsupported, MAX_TOTAL, MAX_DOCUMENT
from reference.core import validate_document
from reference.continuation import inspect_session, inspect_report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('validate','request','restore-workspace','audit-redaction'):
        p=sub.add_parser(name);p.add_argument('session',type=Path)
        if name=='request':p.add_argument('context_id')
        elif name=='restore-workspace':
            p.add_argument('workspace_id');p.add_argument('destination',type=Path)
            p.add_argument('--case-insensitive',action='store_true');p.add_argument('--normalization',choices=['none','NFC','NFD'],default='none')
        elif name=='audit-redaction':p.add_argument('--patterns',type=Path,required=True,help='JSON array of exact strings; values are never included in findings')
    p=sub.add_parser('validate-report');p.add_argument('session',type=Path);p.add_argument('report',type=Path);p.add_argument('--at',help='Assessment time, ISO 8601 with timezone; defaults to current time')
    p=sub.add_parser('pack');p.add_argument('session',type=Path);p.add_argument('output',type=Path)
    for name in ('verify-package','sign','verify-signature'):
        p=sub.add_parser(name);p.add_argument('package',type=Path)
        if name=='sign':p.add_argument('--private-key',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
        elif name=='verify-signature':p.add_argument('--signature',type=Path,required=True);p.add_argument('--trusted-public-key',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command in ('pack','verify-package','sign','verify-signature'):
            from reference.package import package_bytes, inspect_package, signature, verify_signature, write_new
            if args.command=='pack':
                raw=package_bytes(args.session);inspect_package(raw);write_new(args.output,raw);result={'status':'packed','bytes':len(raw),'output':str(args.output)}
            else:
                raw=read(args.package,MAX_TOTAL+MAX_DOCUMENT)
                if args.command=='verify-package':result={'status':'integrity_verified','members':len(inspect_package(raw)),'scope':'container, inventory, session shape and file-backed resource integrity; no authenticity or continuation claim'}
                elif args.command=='sign':
                    write_new(args.output,signature(raw,read(args.private_key,32)));result={'status':'signed','output':str(args.output)}
                else:result=verify_signature(raw,read(args.signature),read(args.trusted_public_key,32))
        else:
            doc,raw=load(args.session);validated=validate_document(doc,args.session.parent)
            if 'continuation' in doc:inspect_session(doc,args.session.parent)
            if args.command=='validate':
                result={'status':'checked','scope':'structure and implemented semantic checks; not full conformance','unsupported_features':validated['unsupported_features'],'streams':validated['streams'],'operational_authorization':False}
            elif args.command=='validate-report':
                report,_=load(args.report);now=datetime.fromisoformat(args.at.replace('Z','+00:00')) if args.at else datetime.now(timezone.utc)
                if now.tzinfo is None:raise Invalid('assessment time needs timezone')
                result=inspect_report(doc,raw,report,args.session.parent,now=now)
            elif args.command=='request':
                from reference.context import reconstruct_request
                result=reconstruct_request(doc,validated,args.context_id)
            elif args.command=='restore-workspace':
                from reference.workspace import restore
                if 'continuation' not in doc:raise Invalid('continuation profile absent')
                if validated['unsupported_features']:raise Unsupported('required feature unsupported')
                result=restore(doc,validated,args.workspace_id,args.destination,case_sensitive=not args.case_insensitive,normalization=args.normalization)
            else:
                from reference.redaction import audit
                patterns,_=load(args.patterns);result=audit(raw,validated,patterns)
        sys.stdout.buffer.write(encode(result))
        if args.command=='validate' and result['unsupported_features']:return 3
        if args.command=='audit-redaction' and result['findings']:return 1
        return 0
    except Unsupported as exc:
        sys.stdout.buffer.write(encode({'status':'unsupported','reason':str(exc)}));return 3
    except (ValidationError,SchemaError) as exc:
        # Do not echo potentially sensitive instance values in exception output.
        sys.stdout.buffer.write(encode({'status':'invalid','reason':'schema validation failed','schema_path':[str(x) for x in exc.absolute_schema_path]}));return 2
    except (Invalid,OSError,ValueError,KeyError,TypeError) as exc:
        reason=str(exc) if isinstance(exc,Invalid) else type(exc).__name__
        sys.stdout.buffer.write(encode({'status':'invalid','reason':reason}));return 2

if __name__=='__main__':raise SystemExit(main())
