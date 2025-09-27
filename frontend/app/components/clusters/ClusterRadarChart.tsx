"use client";

import React, { useEffect, useRef } from 'react';

interface ClusterData {
  cluster_id: string;
  name: string;
  biomarkers: string[];
  description: string;
  severity: string;
  confidence: number;
}

interface ClusterRadarChartProps {
  clusters: ClusterData[];
  biomarkerScores?: Record<string, number>;
  width?: number;
  height?: number;
  className?: string;
}

const ClusterRadarChart: React.FC<ClusterRadarChartProps> = ({
  clusters,
  biomarkerScores = {},
  width = 400,
  height = 400,
  className = ""
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || clusters.length === 0) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = width;
    canvas.height = height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Chart configuration
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;
    const maxClusters = Math.max(6, clusters.length);

    // Color palette for different severities
    const severityColors = {
      critical: '#dc2626', // red-600
      high: '#ea580c',     // orange-600
      moderate: '#d97706', // amber-600
      mild: '#ca8a04',     // yellow-600
      normal: '#16a34a',   // green-600
      default: '#6b7280'   // gray-500
    };

    // Draw background circles
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    for (let i = 1; i <= 5; i++) {
      ctx.beginPath();
      ctx.arc(centerX, centerY, (radius * i) / 5, 0, 2 * Math.PI);
      ctx.stroke();
    }

    // Draw radial lines
    for (let i = 0; i < maxClusters; i++) {
      const angle = (i * 2 * Math.PI) / maxClusters - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    }

    // Draw cluster data
    clusters.forEach((cluster, index) => {
      if (index >= maxClusters) return;

      const angle = (index * 2 * Math.PI) / maxClusters - Math.PI / 2;
      const confidenceRadius = (cluster.confidence * radius) / 5;
      const x = centerX + confidenceRadius * Math.cos(angle);
      const y = centerY + confidenceRadius * Math.sin(angle);

      // Get color based on severity
      const color = severityColors[cluster.severity as keyof typeof severityColors] || severityColors.default;

      // Draw cluster point
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, 2 * Math.PI);
      ctx.fill();

      // Draw confidence ring
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 12, 0, 2 * Math.PI);
      ctx.stroke();

      // Draw cluster name
      ctx.fillStyle = '#374151';
      ctx.font = '12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      const labelX = centerX + (radius + 30) * Math.cos(angle);
      const labelY = centerY + (radius + 30) * Math.sin(angle);
      
      ctx.fillText(cluster.name, labelX, labelY);
    });

    // Draw legend
    const legendY = height - 100;
    ctx.font = '14px Inter, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillStyle = '#374151';
    ctx.fillText('Cluster Severity:', 20, legendY);

    const legendItems = [
      { label: 'Critical', color: severityColors.critical },
      { label: 'High', color: severityColors.high },
      { label: 'Moderate', color: severityColors.moderate },
      { label: 'Mild', color: severityColors.mild },
      { label: 'Normal', color: severityColors.normal }
    ];

    legendItems.forEach((item, index) => {
      const y = legendY + 20 + (index * 20);
      
      // Draw color box
      ctx.fillStyle = item.color;
      ctx.fillRect(20, y - 8, 12, 12);
      
      // Draw label
      ctx.fillStyle = '#374151';
      ctx.fillText(item.label, 40, y);
    });

  }, [clusters, biomarkerScores, width, height]);

  if (clusters.length === 0) {
    return (
      <div className={`flex items-center justify-center ${className}`} style={{ width, height }}>
        <div className="text-center text-gray-500">
          <div className="text-lg font-medium mb-2">No Clusters Found</div>
          <div className="text-sm">Run analysis to generate biomarker clusters</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg border border-gray-200 p-4 ${className}`}>
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Biomarker Clusters</h3>
        <p className="text-sm text-gray-600">
          {clusters.length} cluster{clusters.length !== 1 ? 's' : ''} identified
        </p>
      </div>
      
      <div className="flex justify-center">
        <canvas
          ref={canvasRef}
          className="border border-gray-200 rounded"
        />
      </div>
      
      <div className="mt-4 text-xs text-gray-500 text-center">
        * Cluster size represents confidence level (0-1)
      </div>
    </div>
  );
};

export default ClusterRadarChart;
