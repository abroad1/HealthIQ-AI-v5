'use client';

import React from 'react';
import { pingHealth, openAnalysisSSE, startAnalysis, getAnalysisResult } from '../lib/api';
import { useAnalysisStore } from '../state/analysisStore';
import { useClusterStore } from '../state/clusterStore';
import { useUIStore } from '../state/uiStore';

export default function DevApiProbe() {
  const [status, setStatus] = React.useState<string>('idle');
  const [logs, setLogs] = React.useState<string[]>([]);
  const [analysisId, setAnalysisId] = React.useState<string | null>(null);
  const esRef = React.useRef<EventSource | null>(null);

  // Zustand store hooks
  const analysisStore = useAnalysisStore();
  const clusterStore = useClusterStore();
  const uiStore = useUIStore();

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
        user: { age: 58, sex: 'male' as const },
      };
      
      log('Starting analysis with payload: ' + JSON.stringify(payload));
      
      // Use the new async startAnalysis method
      await analysisStore.startAnalysis(payload);
      
      uiStore.addToast({
        type: 'info',
        title: 'Analysis Started',
        message: 'Biomarker analysis has been initiated',
        duration: 3000,
        position: 'top-right',
      });
      
      // The analysis store now handles SSE internally, so we just log the current state
      const currentAnalysis = analysisStore.currentAnalysis;
      if (currentAnalysis) {
        setAnalysisId(currentAnalysis.analysis_id);
        log('Analysis started with ID: ' + currentAnalysis.analysis_id);
      }
    } catch (e: any) {
      log('startAnalysis ERROR: ' + (e?.message || String(e)));
      
      // Update store with error
      if (analysisId) {
        analysisStore.failAnalysis(analysisId, {
          message: e?.message || String(e),
          code: 'ANALYSIS_START_ERROR',
        });
      }
      
      uiStore.addToast({
        type: 'error',
        title: 'Analysis Failed',
        message: 'Failed to start biomarker analysis',
        duration: 5000,
        position: 'top-right',
      });
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
    <div style={{position:'fixed', right:16, bottom:16, zIndex:9999, maxWidth:500}}
         className="rounded-xl border p-3 shadow bg-white/90 backdrop-blur">
      <div className="flex items-center justify-between gap-2 mb-2">
        <strong>Dev API Probe + Store State</strong>
        <span style={{fontSize:12, opacity:.7}}>status: {status}</span>
      </div>
      
      {/* Store State Display */}
      <div className="mb-3 p-2 bg-gray-50 rounded text-xs">
        <div className="font-semibold mb-1">Store States:</div>
        <div><strong>Analysis:</strong> {analysisStore.currentPhase} ({analysisStore.progress}%)</div>
        <div><strong>Clusters:</strong> {clusterStore.clusters.length} loaded</div>
        <div><strong>UI:</strong> {uiStore.toasts.length} toasts, {uiStore.notifications.length} notifications</div>
        <div><strong>Theme:</strong> {uiStore.actualTheme}</div>
      </div>
      
      <div className="flex gap-2 mb-2 flex-wrap">
        <button onClick={handlePing} className="px-3 py-1 rounded bg-black text-white text-xs">Ping API</button>
        <button onClick={handleStartSSE} className="px-3 py-1 rounded bg-blue-600 text-white text-xs">Start SSE</button>
        <button onClick={handleStopSSE} className="px-3 py-1 rounded bg-gray-200 text-xs">Stop</button>
        <button onClick={handleStartAnalysis} className="px-3 py-1 rounded bg-green-600 text-white text-xs">Start Analysis</button>
        <button onClick={handleFetchResult} className="px-3 py-1 rounded bg-purple-600 text-white text-xs" disabled={!analysisId}>Fetch Result</button>
        <button onClick={() => uiStore.toggleTheme()} className="px-3 py-1 rounded bg-indigo-600 text-white text-xs">Toggle Theme</button>
        <button onClick={() => clusterStore.loadClusters('demo')} className="px-3 py-1 rounded bg-orange-600 text-white text-xs">Load Clusters</button>
      </div>
      
      <div style={{maxHeight:200, overflow:'auto', fontFamily:'ui-monospace, SFMono-Regular, Menlo, monospace', fontSize:12, lineHeight:1.4}}>
        {logs.length === 0 ? <div style={{opacity:.6}}>No logs yet…</div> : logs.map((l,i)=>(<div key={i}>{l}</div>))}
      </div>
      
      <div style={{fontSize:11, opacity:.6, marginTop:6}}>
        Using API_BASE: <code>{process.env.NEXT_PUBLIC_API_BASE ?? 'http://127.0.0.1:8000'}</code>
      </div>
    </div>
  );
}
