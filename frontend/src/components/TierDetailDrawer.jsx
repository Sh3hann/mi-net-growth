import React from 'react';
import { X, Download } from 'lucide-react';

export default function TierDetailDrawer({
  isOpen,
  onClose,
  level,
  onEdit,
  onDelete,
  onDownloadAttachment,
  currentRole,
}) {
  if (!isOpen || !level) return null;

  const isCFO = currentRole === 'CFO';
  const isRM = currentRole === 'RM';

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/30">
      <div className="w-full max-w-md bg-white border-l border-slate-200 shadow-xl flex flex-col h-full overflow-hidden text-xs">
        {/* Header */}
        <div className="p-5 border-b border-slate-200 flex items-center justify-between">
          <div>
            <span className="font-mono font-bold text-slate-900 bg-slate-100 px-2 py-0.5 rounded border border-slate-200 mr-2">
              {level.net_id}
            </span>
            <span className="font-bold text-slate-900 text-sm">{level.level}</span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-600 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-500">Range:</span>
              <span className="font-mono font-medium text-slate-900">
                ${Number(level.lower_range).toLocaleString()} - ${Number(level.upper_range).toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Incentive:</span>
              <span className="font-mono font-bold text-slate-900">{level.percentage}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Status:</span>
              <span className="font-medium text-slate-900">{level.status}</span>
            </div>
          </div>

          {level.attachment && (
            <div className="p-4 rounded-lg border border-slate-200 flex items-center justify-between">
              <span className="truncate text-slate-800">{level.attachment_name}</span>
              <button
                type="button"
                onClick={() => onDownloadAttachment(level.id, level.attachment_name)}
                className="inline-flex items-center gap-1 text-slate-700 hover:text-slate-900 font-medium cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download</span>
              </button>
            </div>
          )}

          {level.comments && (
            <div>
              <span className="text-slate-500 block mb-1 font-medium">Comments:</span>
              <p className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-slate-700">
                {level.comments}
              </p>
            </div>
          )}

          <div className="pt-3 border-t border-slate-200 text-slate-500 space-y-1">
            <div className="flex justify-between">
              <span>Created:</span>
              <span>{level.created_date ? new Date(level.created_date).toLocaleString() : '—'}</span>
            </div>
            <div className="flex justify-between">
              <span>User:</span>
              <span>{level.created_user || 'SYSTEM'}</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
          >
            Close
          </button>
          <button
            type="button"
            onClick={() => {
              onClose();
              onEdit(level);
            }}
            disabled={isRM}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium disabled:opacity-40 cursor-pointer"
          >
            Edit
          </button>
          <button
            type="button"
            onClick={() => {
              onClose();
              onDelete(level);
            }}
            disabled={!isCFO}
            className="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-white font-medium disabled:opacity-40 cursor-pointer"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
