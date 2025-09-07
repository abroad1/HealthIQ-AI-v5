import React from 'react';
import { pingHealth, openAnalysisSSE, startAnalysis, getAnalysisResult } from '../lib/api';

export default function DevApiProbe() {
  const [status, setStatus] = React.useState<string>('idle');
  const [logs, setLogs] = React.useState<string[]>([]);
  const [analysisId, setAnalysisId] = React.useState<string | null>(null);
  const esRef = React.useRef<EventSource | null>(null);

  function log(line: string) {
    setLogs((prev) => [new Date().toLocaleTimeString() + ' — ' + line, ...prev].slice(0, 200));
  }

  async function handlePing() {
    setStatus('pinging');
    try {
      const data = await pingHealth();
      log('health: ' + JSON.stringify(data));
      setStatus('ok');
    } catch (e: any) {
      log('health ERROR: ' + (e?.message || String(e)));
      setStatus('error');
    }
  }

  function handleStartSSE() {
    if (esRef.current) esRef.current.close();
   const es = openAnalysisSSE('demo');
    esRef.current = es;
    es.onopen = () => log('[SSE] open');
    es.onerror = (e) => log('[SSE] error');
    es.addEventListener('analysis_status', (evt) => {
      try {
        const data = JSON.parse((evt as MessageEvent).data);
        log('[SSE] ' + data.phase + ' ' + (data.progress?.toFixed?.(2) ?? ''));
        if (data.phase === 'complete') {
          es.close();
          log('[SSE] closed (complete)');
        }
      } catch {
        log('[SSE] parse error');
      }
    });
  }

  function handleStopSSE() {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
      log('[SSE] closed (manual)');
    }
  }

  async function handleStartAnalysis() {
    try {
      const payload = {
        biomarkers: {
          // use a couple of aliases/on-purpose mixed keys
          cholesterol: { value: 4.9, unit: 'mmol/L' },
          blood_sugar: { value: 4.8, unit: 'mmol/L' },
        },
        user: { age: 58, sex: 'male' },
      };
      const { analysis_id } = await startAnalysis(payload);
      setAnalysisId(analysis_id);
      log('startAnalysis: ' + analysis_id);
      // stream for this analysis id
      if (esRef.current) esRef.current.close();
      const es = openAnalysisSSE(analysis_id);
      esRef.current = es;
      es.onopen = () => log('[SSE] open');
      es.onerror = () => log('[SSE] error');
      es.addEventListener('analysis_status', (evt) => {
        const data = JSON.parse((evt as MessageEvent).data);
        log('[SSE] ' + data.phase + ' ' + (data.progress?.toFixed?.(2) ?? ''));
        if (data.phase === 'complete') {
          es.close();
          log('[SSE] closed (complete)');
        }
      });
    } catch (e: any) {
      log('startAnalysis ERROR: ' + (e?.message || String(e)));
    }
  }

  async function handleFetchResult() {
    if (!analysisId) { log('No analysisId yet'); return; }
    try {
      const data = await getAnalysisResult(analysisId);
      log('result: ' + JSON.stringify(data));
    } catch (e: any) {
      log('getAnalysisResult ERROR: ' + (e?.message || String(e)));
    }
  }

  React.useEffect(() => {
    return () => { if (esRef.current) esRef.current.close(); };
  }, []);

  return (
    <div style={{position:'fixed', right:16, bottom:16, zIndex:9999, maxWidth:420}}
         className="rounded-xl border p-3 shadow bg-white/90 backdrop-blur">
      <div className="flex items-center justify-between gap-2 mb-2">
        <strong>Dev API Probe</strong>
        <span style={{fontSize:12, opacity:.7}}>status: {status}</span>
      </div>
      <div className="flex gap-2 mb-2">
        <button onClick={handlePing} className="px-3 py-1 rounded bg-black text-white">Ping API</button>
        <button onClick={handleStartSSE} className="px-3 py-1 rounded bg-blue-600 text-white">Start SSE</button>
        <button onClick={handleStopSSE} className="px-3 py-1 rounded bg-gray-200">Stop</button>
        <button onClick={handleStartAnalysis} className="px-3 py-1 rounded bg-green-600 text-white">Start Analysis (POST)</button>
        <button onClick={handleFetchResult} className="px-3 py-1 rounded bg-purple-600 text-white" disabled={!analysisId}>Fetch Result</button>
      </div>
      <div style={{maxHeight:200, overflow:'auto', fontFamily:'ui-monospace, SFMono-Regular, Menlo, monospace', fontSize:12, lineHeight:1.4}}>
        {logs.length === 0 ? <div style={{opacity:.6}}>No logs yet…</div> : logs.map((l,i)=>(<div key={i}>{l}</div>))}
      </div>
      <div style={{fontSize:11, opacity:.6, marginTop:6}}>
        Using API_BASE: <code>{(import.meta as any).env?.VITE_API_BASE ?? 'http://127.0.0.1:8000'}</code>
      </div>
    </div>
  );
}
