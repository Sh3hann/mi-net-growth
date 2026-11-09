import React, { useState, useEffect } from 'react';
import { X, Upload, FileCheck, AlertCircle, AlertTriangle } from 'lucide-react';

export default function LevelFormModal({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  existingLevels,
  submitting,
}) {
  const isEditing = Boolean(initialData && initialData.id);

  const [formData, setFormData] = useState({
    level: '',
    lower_range: '',
    upper_range: '',
    percentage: '',
    status: 'Active',
    comments: '',
  });

  const [selectedFile, setSelectedFile] = useState(null);
  const [filePreviewName, setFilePreviewName] = useState('');
  const [clientErrors, setClientErrors] = useState({});
  const [overlapWarning, setOverlapWarning] = useState('');

  useEffect(() => {
    if (initialData) {
      setFormData({
        level: initialData.level || '',
        lower_range: initialData.lower_range || '',
        upper_range: initialData.upper_range || '',
        percentage: initialData.percentage || '',
        status: initialData.status || 'Active',
        comments: initialData.comments || '',
      });
      setSelectedFile(null);
      setFilePreviewName(initialData.attachment_name || '');
    } else {
      setFormData({
        level: '',
        lower_range: '',
        upper_range: '',
        percentage: '',
        status: 'Active',
        comments: '',
      });
      setSelectedFile(null);
      setFilePreviewName('');
    }
    setClientErrors({});
    setOverlapWarning('');
  }, [initialData, isOpen]);

  useEffect(() => {
    const lower = parseFloat(formData.lower_range);
    const upper = parseFloat(formData.upper_range);
    const pct = parseFloat(formData.percentage);
    const errors = {};
    let overlapMsg = '';

    if (formData.lower_range !== '' && !isNaN(lower)) {
      if (lower < 0) {
        errors.lower_range = 'Lower Range cannot be negative';
      }
    }

    if (formData.upper_range !== '' && !isNaN(upper) && !isNaN(lower)) {
      if (upper <= lower) {
        errors.upper_range = 'Upper Range must be greater than Lower Range';
      }
    }

    if (formData.percentage !== '' && !isNaN(pct)) {
      if (pct < 0 || pct > 100) {
        errors.percentage = 'Percentage must be between 0 and 100';
      }
    }

    // Overlap validation
    if (
      formData.status === 'Active' &&
      !isNaN(lower) &&
      !isNaN(upper) &&
      upper > lower &&
      existingLevels &&
      existingLevels.length > 0
    ) {
      const currentId = initialData?.id;
      const conflicts = existingLevels.filter((lvl) => {
        if (lvl.id === currentId || lvl.status !== 'Active') return false;
        const oLower = parseFloat(lvl.lower_range);
        const oUpper = parseFloat(lvl.upper_range);
        return lower <= oUpper && upper >= oLower;
      });

      if (conflicts.length > 0) {
        const names = conflicts
          .map((c) => `${c.net_id} ($${Number(c.lower_range).toLocaleString()} - $${Number(c.upper_range).toLocaleString()})`)
          .join(', ');
        overlapMsg = `Warning: Range overlaps with active level ${names}`;
      }
    }

    setClientErrors(errors);
    setOverlapWarning(overlapMsg);
  }, [formData, existingLevels, initialData]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setFilePreviewName(file.name);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setFilePreviewName('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const errors = {};
    if (!formData.level.trim()) {
      errors.level = 'Level is required';
    }
    if (formData.lower_range === '') {
      errors.lower_range = 'Lower Range is required';
    }
    if (formData.upper_range === '') {
      errors.upper_range = 'Upper Range is required';
    }
    if (formData.percentage === '') {
      errors.percentage = 'Percentage is required';
    }

    if (Object.keys(errors).length > 0 || Object.keys(clientErrors).length > 0 || overlapWarning) {
      setClientErrors((prev) => ({ ...prev, ...errors }));
      return;
    }

    const payload = new FormData();
    payload.append('level', formData.level.trim());
    payload.append('lower_range', formData.lower_range);
    payload.append('upper_range', formData.upper_range);
    payload.append('percentage', formData.percentage);
    payload.append('status', formData.status);
    if (formData.comments) {
      payload.append('comments', formData.comments.trim());
    }
    if (selectedFile) {
      payload.append('attachment', selectedFile);
    }

    onSubmit(payload, isEditing ? initialData.id : null);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 animate-fade-in">
      <div className="bg-white rounded-xl shadow-xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header - Clean, no subtitle clutter */}
        <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-900">
            {isEditing ? `Edit Level (${initialData?.net_id})` : 'Add New Level'}
          </h3>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-600 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-5 overflow-y-auto space-y-4 text-xs">
          {overlapWarning && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-500 flex-shrink-0 mt-0.5" />
              <span>{overlapWarning}</span>
            </div>
          )}

          {/* Level Name */}
          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Level Name <span className="text-rose-500">*</span>
            </label>
            <input
              type="text"
              name="level"
              value={formData.level}
              onChange={handleChange}
              placeholder="e.g. Bronze Foundation"
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 focus:outline-hidden focus:border-slate-400"
            />
            {clientErrors.level && (
              <p className="text-rose-500 mt-1 flex items-center gap-1">
                <AlertCircle className="w-3.5 h-3.5" /> {clientErrors.level}
              </p>
            )}
          </div>

          {/* Range Inputs */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Lower Range ($) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                name="lower_range"
                value={formData.lower_range}
                onChange={handleChange}
                placeholder="0.00"
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 font-mono focus:outline-hidden focus:border-slate-400"
              />
              {clientErrors.lower_range && (
                <p className="text-rose-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5" /> {clientErrors.lower_range}
                </p>
              )}
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Upper Range ($) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                name="upper_range"
                value={formData.upper_range}
                onChange={handleChange}
                placeholder="50000.00"
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 font-mono focus:outline-hidden focus:border-slate-400"
              />
              {clientErrors.upper_range && (
                <p className="text-rose-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5" /> {clientErrors.upper_range}
                </p>
              )}
            </div>
          </div>

          {/* Percentage & Status */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Percentage (%) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="percentage"
                value={formData.percentage}
                onChange={handleChange}
                placeholder="5.00"
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 font-mono focus:outline-hidden focus:border-slate-400"
              />
              {clientErrors.percentage && (
                <p className="text-rose-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5" /> {clientErrors.percentage}
                </p>
              )}
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                Status
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 focus:outline-hidden focus:border-slate-400 cursor-pointer"
              >
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
          </div>

          {/* File Upload */}
          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Attachment (Optional)
            </label>
            <div className="border border-slate-200 rounded-lg p-3 bg-slate-50">
              {filePreviewName ? (
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-800 truncate">
                    {filePreviewName}
                  </span>
                  <button
                    type="button"
                    onClick={handleRemoveFile}
                    className="text-slate-400 hover:text-slate-700 text-xs cursor-pointer"
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <label className="flex items-center gap-2 cursor-pointer text-slate-600 hover:text-slate-900">
                  <Upload className="w-4 h-4 text-slate-400" />
                  <span>Choose file...</span>
                  <input type="file" onChange={handleFileChange} className="hidden" />
                </label>
              )}
            </div>
          </div>

          {/* Comments */}
          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Comments (Optional)
            </label>
            <input
              type="text"
              name="comments"
              value={formData.comments}
              onChange={handleChange}
              placeholder="Optional notes..."
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 focus:outline-hidden focus:border-slate-400"
            />
          </div>

          {/* Footer Actions - Solid black primary button, white cancel button */}
          <div className="pt-3 border-t border-slate-200 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="px-3 py-2 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || Boolean(overlapWarning)}
              className="px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium disabled:opacity-50 transition-colors cursor-pointer"
            >
              {submitting ? 'Saving...' : isEditing ? 'Update Level' : 'Save Level'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
