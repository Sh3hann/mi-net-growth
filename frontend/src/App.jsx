import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import StatsCards from './components/StatsCards';
import RangeVisualizer from './components/RangeVisualizer';
import FilterBar from './components/FilterBar';
import GrowthLevelTable from './components/GrowthLevelTable';
import LevelFormModal from './components/LevelFormModal';
import DeleteConfirmModal from './components/DeleteConfirmModal';
import TierDetailDrawer from './components/TierDetailDrawer';
import SimulatorModal from './components/SimulatorModal';
import Toast from './components/Toast';
import { growthLevelsApi, formatApiError } from './services/api';

export default function App() {
  const [currentRole, setCurrentRole] = useState(
    () => localStorage.getItem('mi_growth_user_role') || 'CFO'
  );

  const [levels, setLevels] = useState([]);
  const [allActiveLevels, setAllActiveLevels] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [paginationInfo, setPaginationInfo] = useState({
    count: 0,
    totalPages: 1,
    currentPage: 1,
    pageSize: 10,
    next: null,
    previous: null,
  });

  const [formModalOpen, setFormModalOpen] = useState(false);
  const [editingLevel, setEditingLevel] = useState(null);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [deletingLevel, setDeletingLevel] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [inspectingLevel, setInspectingLevel] = useState(null);
  const [simulatorOpen, setSimulatorOpen] = useState(false);

  const [submitting, setSubmitting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [toasts, setToasts] = useState([]);

  const addToast = (type, message, title = '') => {
    const id = Date.now() + Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, type, message, title }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const handleRoleChange = (newRole) => {
    setCurrentRole(newRole);
    localStorage.setItem('mi_growth_user_role', newRole);
    localStorage.setItem('mi_growth_user_name', `${newRole}_User`);
    addToast('info', `Switched role to ${newRole}`);
  };

  const fetchStats = useCallback(async () => {
    try {
      const data = await growthLevelsApi.getStatistics();
      setStats(data);
    } catch (err) {
      console.error(err);
    }
  }, []);

  const fetchAllActive = useCallback(async () => {
    try {
      const data = await growthLevelsApi.getAll({ paginate: 'false' });
      setAllActiveLevels(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      console.error(err);
    }
  }, []);

  const fetchLevels = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page,
        page_size: pageSize,
      };
      if (statusFilter !== 'All') {
        params.status = statusFilter;
      }
      if (search.trim()) {
        params.search = search.trim();
      }

      const response = await growthLevelsApi.getAll(params);

      if (response && response.results) {
        setLevels(response.results);
        setPaginationInfo({
          count: response.count,
          totalPages: response.total_pages,
          currentPage: response.current_page,
          pageSize,
          next: response.next,
          previous: response.previous,
        });
      } else if (Array.isArray(response)) {
        setLevels(response);
        setPaginationInfo({
          count: response.length,
          totalPages: 1,
          currentPage: 1,
          pageSize: response.length,
          next: null,
          previous: null,
        });
      }
    } catch (err) {
      const errorMsg = formatApiError(err);
      addToast('error', errorMsg);
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, statusFilter, search]);

  useEffect(() => {
    fetchLevels();
  }, [fetchLevels]);

  useEffect(() => {
    fetchStats();
    fetchAllActive();
  }, [fetchStats, fetchAllActive]);

  const handleSearchChange = (val) => {
    setSearch(val);
    setPage(1);
  };

  const handleStatusFilterChange = (val) => {
    setStatusFilter(val);
    setPage(1);
  };

  const handleOpenAddModal = () => {
    if (currentRole === 'RM') {
      addToast('warning', 'RM has read-only access');
      return;
    }
    setEditingLevel(null);
    setFormModalOpen(true);
  };

  const handleOpenEditModal = (level) => {
    if (currentRole === 'RM') {
      addToast('warning', 'RM cannot edit records');
      return;
    }
    setEditingLevel(level);
    setFormModalOpen(true);
  };

  const handleInspect = (level) => {
    setInspectingLevel(level);
    setDrawerOpen(true);
  };

  const handleSubmitForm = async (formData, id) => {
    setSubmitting(true);
    try {
      if (id) {
        await growthLevelsApi.update(id, formData);
        addToast('success', 'Level updated successfully');
      } else {
        await growthLevelsApi.create(formData);
        addToast('success', 'Level created successfully');
      }
      setFormModalOpen(false);
      fetchLevels();
      fetchStats();
      fetchAllActive();
    } catch (err) {
      const errorMsg = formatApiError(err);
      addToast('error', errorMsg);
    } finally {
      setSubmitting(false);
    }
  };

  const handleOpenDeleteModal = (level) => {
    if (currentRole !== 'CFO') {
      addToast('warning', 'Only CFO can delete records');
      return;
    }
    setDeletingLevel(level);
    setDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!deletingLevel) return;
    setIsDeleting(true);
    try {
      await growthLevelsApi.delete(deletingLevel.id);
      addToast('success', 'Level deleted');
      setDeleteModalOpen(false);
      setDeletingLevel(null);
      if (inspectingLevel?.id === deletingLevel.id) {
        setDrawerOpen(false);
      }
      fetchLevels();
      fetchStats();
      fetchAllActive();
    } catch (err) {
      const errorMsg = formatApiError(err);
      addToast('error', errorMsg);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDownloadAttachment = async (id, filename) => {
    try {
      await growthLevelsApi.downloadAttachment(id, filename);
    } catch (err) {
      const errorMsg = formatApiError(err);
      addToast('error', errorMsg);
    }
  };

  const handleExportCsv = () => {
    if (!levels || levels.length === 0) {
      addToast('warning', 'No data to export');
      return;
    }
    const headers = [
      'ID',
      'NET_ID',
      'LEVEL',
      'LOWER_RANGE',
      'UPPER_RANGE',
      'PERCENTAGE',
      'STATUS',
      'CREATED_USER',
      'UPDATED_USER',
      'COMMENTS',
    ];
    const rows = levels.map((l) => [
      l.id,
      `"${l.net_id}"`,
      `"${l.level}"`,
      l.lower_range,
      l.upper_range,
      l.percentage,
      l.status,
      `"${l.created_user || ''}"`,
      `"${l.updated_user || ''}"`,
      `"${(l.comments || '').replace(/"/g, '""')}"`,
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `MI_Net_Growth_Levels_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    addToast('success', 'Exported to CSV');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col antialiased">
      {/* Top Navbar */}
      <Navbar
        currentRole={currentRole}
        onRoleChange={handleRoleChange}
        onOpenSimulator={() => setSimulatorOpen(true)}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-5">
        {/* Metric Cards */}
        <StatsCards stats={stats} loading={loading && !stats} />

        {/* Range Coverage Bar */}
        <RangeVisualizer
          levels={allActiveLevels}
          onSelectTier={(tier) => handleInspect(tier)}
        />

        {/* Toolbar */}
        <FilterBar
          search={search}
          onSearchChange={handleSearchChange}
          statusFilter={statusFilter}
          onStatusFilterChange={handleStatusFilterChange}
          onAddNew={handleOpenAddModal}
          onRefresh={() => {
            fetchLevels();
            fetchStats();
            fetchAllActive();
            addToast('info', 'Data refreshed');
          }}
          onExportCsv={handleExportCsv}
          loading={loading}
          currentRole={currentRole}
        />

        {/* Data Table */}
        <GrowthLevelTable
          levels={levels}
          loading={loading}
          onEdit={handleOpenEditModal}
          onDelete={handleOpenDeleteModal}
          onDownloadAttachment={handleDownloadAttachment}
          currentRole={currentRole}
          pagination={paginationInfo}
          onPageChange={(newPage) => setPage(newPage)}
          onPageSizeChange={(newSize) => {
            setPageSize(newSize);
            setPage(1);
          }}
        />
      </main>

      {/* Modals & Drawer */}
      <TierDetailDrawer
        isOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        level={inspectingLevel}
        onEdit={handleOpenEditModal}
        onDelete={handleOpenDeleteModal}
        onDownloadAttachment={handleDownloadAttachment}
        currentRole={currentRole}
      />

      <SimulatorModal
        isOpen={simulatorOpen}
        onClose={() => setSimulatorOpen(false)}
        activeLevels={allActiveLevels}
      />

      <LevelFormModal
        isOpen={formModalOpen}
        onClose={() => setFormModalOpen(false)}
        onSubmit={handleSubmitForm}
        initialData={editingLevel}
        existingLevels={allActiveLevels}
        submitting={submitting}
      />

      <DeleteConfirmModal
        isOpen={deleteModalOpen}
        onClose={() => {
          setDeleteModalOpen(false);
          setDeletingLevel(null);
        }}
        onConfirm={handleConfirmDelete}
        levelData={deletingLevel}
        deleting={isDeleting}
      />

      <Toast toasts={toasts} onDismiss={removeToast} />

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 mt-8 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>MI Net Growth Levels Management System</span>
          <span className="font-mono text-slate-400">SIA_MI_NET_GROWTH_LEVELS</span>
        </div>
      </footer>
    </div>
  );
}
