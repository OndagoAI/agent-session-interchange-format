"""Deterministic fragment assembly; no tool execution or external fetches."""
from .common import need, decode, MAX_RESOURCE

def assemble_streams(doc,validated):
    events=validated['collections']['events'];outputs={}
    for stream in doc.get('streams',[]):
        need(stream['id'] not in outputs,'duplicate stream ID');need(stream['event_id'] in events,'missing stream event')
        event=events[stream['event_id']];need(event['data'].get('call_id')==stream['call_id'],'stream call mismatch')
        if stream['kind']=='tool_result_text':need(event['kind']=='tool_result' and event['data']['result_index']==stream['result_index'],'stream result mismatch')
        segments=stream['segments'];indices=[s['index'] for s in segments]
        need(len(indices)==len(set(indices)) and indices==sorted(indices),'duplicate/unordered stream segment')
        need(sum(bool(s['terminal']) for s in segments)<=1,'multiple stream terminal segments')
        if any(s['terminal'] for s in segments):need(segments[-1]['terminal'],'stream terminal before final segment')
        raw=bytearray();expected=0;gap=False
        for segment in segments:
            content=validated['resources'].bytes(segment['resource_id']);start=segment['offset'];end=start+segment['length']
            need(end<=len(content),'stream span outside resource')
            if segment['index']!=expected:gap=True
            if not gap:raw.extend(content[start:end]);expected+=1
            need(len(raw)<=MAX_RESOURCE,'stream assembly byte limit')
        complete=not gap and bool(segments) and segments[-1]['terminal']
        need(stream['status']==('complete' if complete else 'partial'),'stream completeness mismatch')
        if complete and stream['kind']=='tool_arguments':
            need(event['kind']=='tool_call' and event['data']['arguments_status']=='complete','stream final call mismatch')
            need(decode(bytes(raw))==event['data']['arguments'],'assembled arguments mismatch')
        elif complete:
            need(event['kind']=='tool_result' and event['data']['result_index']==stream['result_index'],'stream result mismatch')
            try:text=bytes(raw).decode('utf8')
            except UnicodeError as exc:raise ValueError('stream text is not UTF-8') from exc
            need(event['data']['parts']==[{'kind':'text','text':text}],'assembled result mismatch')
        elif stream['kind']=='tool_arguments':need(event['kind']=='tool_call' and event['data']['arguments_status']=='partial','partial stream presented as executable call')
        outputs[stream['id']]={'status':'complete' if complete else 'partial','contiguous_bytes':len(raw),'executable':False}
    return outputs
