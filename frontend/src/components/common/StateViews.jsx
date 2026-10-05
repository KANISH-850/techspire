import React from 'react';
import { Activity, AlertCircle, Inbox } from 'lucide-react';

export const LoadingView = ({ title = "Loading data..." }) => (
  <div className="flex h-64 w-full items-center justify-center p-6">
    <div className="flex flex-col items-center gap-3">
      <Activity className="w-8 h-8 text-cyan-400 animate-spin" />
      <p className="text-sm font-medium text-[var(--ts-text-secondary)]">{title}</p>
    </div>
  </div>
);

export const ErrorView = ({ error, onRetry }) => (
  <div className="flex h-64 w-full items-center justify-center p-6">
    <div className="bg-[var(--ts-bg-subtle)] border border-rose-500/30 p-6 rounded-2xl max-w-md text-center shadow-xl">
      <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-3" />
      <h3 className="text-lg font-bold text-[var(--ts-text-primary)] mb-1">Failed to Load Data</h3>
      <p className="text-xs text-[var(--ts-text-secondary)] mb-4">{error || "An unexpected network error occurred."}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="ts-btn-primary px-4 py-2 text-xs"
        >
          Retry Request
        </button>
      )}
    </div>
  </div>
);

export const EmptyView = ({ title = "No items found", description = "There is no data to display right now." }) => (
  <div className="flex h-64 w-full items-center justify-center p-6">
    <div className="text-center p-6 max-w-sm">
      <Inbox className="w-12 h-12 text-[var(--ts-text-muted)] mx-auto mb-3 opacity-60" />
      <h4 className="text-base font-semibold text-[var(--ts-text-primary)] mb-1">{title}</h4>
      <p className="text-xs text-[var(--ts-text-muted)]">{description}</p>
    </div>
  </div>
);

export default { LoadingView, ErrorView, EmptyView };
