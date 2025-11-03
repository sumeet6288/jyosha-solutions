import React, { useState, useEffect } from 'react';
import { UserCheck, Shield, Clock, AlertTriangle, Eye, Play, StopCircle } from 'lucide-react';
import { Button } from '../ui/button';

const ImpersonationPanel = ({ backendUrl }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showStartModal, setShowStartModal] = useState(false);
  const [activeSession, setActiveSession] = useState(null);
  
  const [impersonationRequest, setImpersonationRequest] = useState({
    target_user_id: '',
    reason: ''
  });

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/admin/users-enhanced/impersonation-history`);
      const data = await response.json();
      if (data.success) {
        setHistory(data.sessions);
        // Check for active session
        const active = data.sessions.find(s => !s.ended_at);
        if (active) {
          setActiveSession(active);
        }
      }
    } catch (error) {
      console.error('Error fetching impersonation history:', error);
    } finally {
      setLoading(false);
    }
  };

  const startImpersonation = async () => {
    if (!impersonationRequest.target_user_id || !impersonationRequest.reason) {
      alert('Please provide both user ID and reason');
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/admin/users-enhanced/impersonate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(impersonationRequest)
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`Impersonation session started for ${data.target_user.name}`);
        setActiveSession({ id: data.session_id, ...data.target_user });
        setShowStartModal(false);
        setImpersonationRequest({ target_user_id: '', reason: '' });
        fetchHistory();
      }
    } catch (error) {
      console.error('Error starting impersonation:', error);
      alert('Failed to start impersonation session');
    }
  };

  const endImpersonation = async () => {
    if (!activeSession) return;

    try {
      const response = await fetch(`${backendUrl}/api/admin/users-enhanced/impersonate/${activeSession.id}/end`, {
        method: 'POST'
      });
      const data = await response.json();
      
      if (data.success) {
        alert('Impersonation session ended');
        setActiveSession(null);
        fetchHistory();
      }
    } catch (error) {
      console.error('Error ending impersonation:', error);
      alert('Failed to end impersonation session');
    }
  };

  const formatDuration = (startedAt, endedAt) => {
    const start = new Date(startedAt);
    const end = endedAt ? new Date(endedAt) : new Date();
    const minutes = Math.floor((end - start) / 60000);
    return `${minutes} min`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">User Impersonation</h2>
          <p className="text-gray-600">Login as users for support purposes (fully audited)</p>
        </div>
        <Button 
          onClick={() => setShowStartModal(true)} 
          disabled={!!activeSession}
        >
          <Play className="w-4 h-4 mr-2" />
          Start Impersonation
        </Button>
      </div>

      {/* Active Session Alert */}
      {activeSession && (
        <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <Eye className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm opacity-90 font-medium">Active Impersonation Session</p>
                <p className="text-xl font-bold">{activeSession.target_user_email || 'Unknown User'}</p>
                <p className="text-sm opacity-90 mt-1">
                  Started {new Date(activeSession.started_at).toLocaleTimeString()}
                </p>
              </div>
            </div>
            <Button 
              variant="outline" 
              onClick={endImpersonation}
              className="bg-white text-red-600 hover:bg-red-50"
            >
              <StopCircle className="w-4 h-4 mr-2" />
              End Session
            </Button>
          </div>
        </div>
      )}

      {/* Security Warning */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-yellow-800">
            <p className="font-semibold mb-1">Security Notice</p>
            <p>
              All impersonation sessions are fully logged and audited. Only use this feature for legitimate support purposes.
              Unauthorized access or abuse will be tracked and may result in immediate termination.
            </p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <UserCheck className="w-8 h-8 text-blue-600 mb-3" />
          <p className="text-3xl font-bold">{history.length}</p>
          <p className="text-sm text-gray-600">Total Sessions</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <Clock className="w-8 h-8 text-green-600 mb-3" />
          <p className="text-3xl font-bold">
            {history.filter(s => s.ended_at).length}
          </p>
          <p className="text-sm text-gray-600">Completed Sessions</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <AlertTriangle className="w-8 h-8 text-orange-600 mb-3" />
          <p className="text-3xl font-bold">
            {history.filter(s => !s.ended_at).length}
          </p>
          <p className="text-sm text-gray-600">Active Sessions</p>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-bold">Impersonation History</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Admin</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Target User</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Started</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Duration</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {loading ? (
                <tr>
                  <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                    Loading history...
                  </td>
                </tr>
              ) : history.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                    No impersonation sessions yet
                  </td>
                </tr>
              ) : (
                history.map((session) => (
                  <tr key={session.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <p className="font-medium">{session.admin_email}</p>
                      <p className="text-xs text-gray-500">{session.admin_id}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="font-medium">{session.target_user_email}</p>
                      <p className="text-xs text-gray-500">{session.target_user_id}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-sm text-gray-700">{session.reason}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-sm">{new Date(session.started_at).toLocaleString()}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-sm">{formatDuration(session.started_at, session.ended_at)}</p>
                    </td>
                    <td className="px-4 py-3">
                      {session.ended_at ? (
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                          Ended
                        </span>
                      ) : (
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 animate-pulse">
                          Active
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Start Impersonation Modal */}
      {showStartModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-xl font-bold">Start Impersonation Session</h3>
              <p className="text-sm text-gray-600 mt-1">This action will be logged</p>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target User ID
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  placeholder="Enter user ID"
                  value={impersonationRequest.target_user_id}
                  onChange={(e) => setImpersonationRequest({ ...impersonationRequest, target_user_id: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Reason for Impersonation
                </label>
                <textarea
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  rows="3"
                  placeholder="e.g., Customer support ticket #1234"
                  value={impersonationRequest.reason}
                  onChange={(e) => setImpersonationRequest({ ...impersonationRequest, reason: e.target.value })}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Provide a detailed reason for compliance and auditing
                </p>
              </div>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-600 flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-yellow-800">
                    By starting this session, you acknowledge that all actions will be logged and audited.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-gray-200 flex gap-3 justify-end">
              <Button variant="outline" onClick={() => setShowStartModal(false)}>
                Cancel
              </Button>
              <Button 
                onClick={startImpersonation}
                disabled={!impersonationRequest.target_user_id || !impersonationRequest.reason}
              >
                <Play className="w-4 h-4 mr-2" />
                Start Session
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImpersonationPanel;