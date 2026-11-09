import React from 'react';
import { Download, Edit2, Trash2 } from 'lucide-react';

export default function GrowthLevelTable({
  levels,
  loading,
  onEdit,
  onDelete,
  onDownloadAttachment,
  currentRole,
  pagination,
  onPageChange,
  onPageSizeChange,
}) {
  const isCFO = currentRole === 'CFO';
  const isRM = currentRole === 'RM';

  if (loading && (!levels || levels.length === 0)) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-xs">
        <div className="animate-pulse space-y-3">
          <div className="h-5 bg-slate-100 rounded w-1/4" />
          <div className="h-10 bg-slate-100 rounded w-full" />
          <div className="h-10 bg-slate-100 rounded w-full" />
          <div className="h-10 bg-slate-100 rounded w-full" />
        </div>
      </div>
    );
  }

  if (!levels || levels.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-xs">
        <p className="text-sm font-medium text-slate-600">No records found</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
              <th className="py-3 px-4">NET ID</th>
              <th className="py-3 px-4">Level</th>
              <th className="py-3 px-4 text-right">Lower Range</th>
              <th className="py-3 px-4 text-right">Upper Range</th>
              <th className="py-3 px-4 text-center">Incentive</th>
              <th className="py-3 px-4 text-center">Status</th>
              <th className="py-3 px-4">Attachment</th>
              <th className="py-3 px-4">User</th>
              <th className="py-3 px-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-800">
            {levels.map((item) => {
              const isActive = item.status === 'Active';
              const lowerVal = Number(item.lower_range);
              const upperVal = Number(item.upper_range);

              return (
                <tr key={item.id} className="hover:bg-slate-50/70 transition-colors">
                  {/* NET_ID */}
                  <td className="py-3 px-4 font-mono font-semibold text-slate-900 whitespace-nowrap">
                    <span className="px-2 py-0.5 rounded bg-slate-100 border border-slate-200">
                      {item.net_id}
                    </span>
                  </td>

                  {/* Level Name */}
                  <td className="py-3 px-4 font-medium text-slate-900">
                    <div>{item.level}</div>
                    {item.comments && (
                      <div className="text-[11px] text-slate-400 mt-0.5 line-clamp-1 truncate">
                        {item.comments}
                      </div>
                    )}
                  </td>

                  {/* Lower Range */}
                  <td className="py-3 px-4 text-right font-mono tabular-nums whitespace-nowrap">
                    ${lowerVal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>

                  {/* Upper Range */}
                  <td className="py-3 px-4 text-right font-mono tabular-nums whitespace-nowrap">
                    ${upperVal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>

                  {/* Incentive */}
                  <td className="py-3 px-4 text-center font-semibold font-mono tabular-nums whitespace-nowrap">
                    {item.percentage}%
                  </td>

                  {/* Status */}
                  <td className="py-3 px-4 text-center whitespace-nowrap">
                    {isActive ? (
                      <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
                        Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200">
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                        Inactive
                      </span>
                    )}
                  </td>

                  {/* Attachment */}
                  <td className="py-3 px-4 whitespace-nowrap">
                    {item.attachment ? (
                      <button
                        type="button"
                        onClick={() =>
                          onDownloadAttachment(
                            item.id,
                            item.attachment_name || `${item.net_id}_file`
                          )
                        }
                        className="inline-flex items-center gap-1 text-[11px] text-slate-700 hover:text-slate-900 hover:underline cursor-pointer"
                        title={`Download ${item.attachment_name}`}
                      >
                        <Download className="w-3 h-3 text-slate-500" />
                        <span className="max-w-[120px] truncate">
                          {item.attachment_name || 'Download'}
                        </span>
                      </button>
                    ) : (
                      <span className="text-slate-400">—</span>
                    )}
                  </td>

                  {/* User */}
                  <td className="py-3 px-4 text-slate-600 whitespace-nowrap">
                    {item.updated_user || item.created_user || 'SYSTEM'}
                  </td>

                  {/* Actions */}
                  <td className="py-3 px-4 text-center whitespace-nowrap">
                    <div className="inline-flex items-center gap-1">
                      <button
                        type="button"
                        onClick={() => onEdit(item)}
                        disabled={isRM}
                        className="p-1 rounded text-slate-500 hover:text-slate-900 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer"
                        title={isRM ? 'Read-only access' : 'Edit'}
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>

                      <button
                        type="button"
                        onClick={() => onDelete(item)}
                        disabled={!isCFO}
                        className="p-1 rounded text-slate-500 hover:text-rose-600 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer"
                        title={!isCFO ? 'CFO only' : 'Delete'}
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && (
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 px-4 py-3 bg-slate-50 border-t border-slate-200 text-xs text-slate-600">
          <div className="flex items-center gap-2">
            <span>
              Total <strong>{pagination.count || 0}</strong> records
            </span>
            <span>•</span>
            <div className="flex items-center gap-1">
              <span>Show:</span>
              <select
                value={pagination.pageSize || 10}
                onChange={(e) => onPageSizeChange(Number(e.target.value))}
                className="bg-white border border-slate-200 rounded px-1.5 py-0.5 text-xs font-medium text-slate-700 cursor-pointer"
              >
                <option value={5}>5</option>
                <option value={10}>10</option>
                <option value={25}>25</option>
                <option value={50}>50</option>
              </select>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span>
              Page {pagination.currentPage || 1} of {pagination.totalPages || 1}
            </span>
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => onPageChange(pagination.currentPage - 1)}
                disabled={!pagination.previous || loading}
                className="px-2.5 py-1 rounded border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                Previous
              </button>
              <button
                type="button"
                onClick={() => onPageChange(pagination.currentPage + 1)}
                disabled={!pagination.next || loading}
                className="px-2.5 py-1 rounded border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
