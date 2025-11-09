import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { FileText, Search, Filter, ArrowLeft, Trash2, Plus, Edit, Lock, TrendingUp, X } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import ResponsiveNav from '../components/ResponsiveNav';
import { useAuth } from '../contexts/AuthContext';

const Leads = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { user, logout } = useAuth();
  const [leads, setLeads] = useState([]);
  const [leadsData, setLeadsData] = useState({});
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedLead, setSelectedLead] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    status: 'active',
    notes: ''
  });
  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/leads/leads`, {
        credentials: 'include'
      });
      const data = await response.json();
      setLeads(data.leads || []);
      setLeadsData(data);
    } catch (error) {
      console.error('Error fetching leads:', error);
      toast({
        title: 'Error',
        description: 'Failed to load leads',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddLead = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/leads/leads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: 'Success',
          description: 'Lead added successfully'
        });
        setShowAddModal(false);
        setFormData({
          name: '',
          email: '',
          phone: '',
          company: '',
          status: 'active',
          notes: ''
        });
        fetchLeads();
      } else if (response.status === 403) {
        toast({
          title: 'Limit Reached',
          description: data.detail?.message || 'You have reached your lead limit',
          variant: 'destructive'
        });
      } else {
        throw new Error('Failed to add lead');
      }
    } catch (error) {
      console.error('Error adding lead:', error);
      toast({
        title: 'Error',
        description: 'Failed to add lead',
        variant: 'destructive'
      });
    }
  };

  const handleUpdateLead = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/leads/leads/${selectedLead.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        toast({
          title: 'Success',
          description: 'Lead updated successfully'
        });
        setShowEditModal(false);
        setSelectedLead(null);
        setFormData({
          name: '',
          email: '',
          phone: '',
          company: '',
          status: 'active',
          notes: ''
        });
        fetchLeads();
      } else {
        throw new Error('Failed to update lead');
      }
    } catch (error) {
      console.error('Error updating lead:', error);
      toast({
        title: 'Error',
        description: 'Failed to update lead',
        variant: 'destructive'
      });
    }
  };

  const handleDeleteLead = async (leadId) => {
    if (!window.confirm('Are you sure you want to delete this lead?')) {
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/leads/leads/${leadId}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      if (response.ok) {
        toast({
          title: 'Success',
          description: 'Lead deleted successfully'
        });
        fetchLeads();
      } else {
        throw new Error('Failed to delete lead');
      }
    } catch (error) {
      console.error('Error deleting lead:', error);
      toast({
        title: 'Error',
        description: 'Failed to delete lead',
        variant: 'destructive'
      });
    }
  };

  const handleEditClick = (lead) => {
    setSelectedLead(lead);
    setFormData({
      name: lead.name || '',
      email: lead.email || '',
      phone: lead.phone || '',
      company: lead.company || '',
      status: lead.status || 'active',
      notes: lead.notes || ''
    });
    setShowEditModal(true);
  };

  const handleLogout = () => {
    logout();
    toast({
      title: 'Signed out',
      description: 'You have been signed out successfully'
    });
    navigate('/signin');
  };

  const filteredLeads = leads.filter(lead => {
    if (!searchQuery) return true;
    const search = searchQuery.toLowerCase();
    return (
      lead.name?.toLowerCase().includes(search) ||
      lead.email?.toLowerCase().includes(search) ||
      lead.phone?.toLowerCase().includes(search) ||
      lead.company?.toLowerCase().includes(search)
    );
  });

  const planName = leadsData.plan_name || 'Free';
  const isFree = planName === 'Free' || planName === 'Free Plan';
  const isStarter = planName === 'Starter' || planName === 'Starter Plan';
  const isProfessional = planName === 'Professional' || planName === 'Professional Plan';
  const currentLeads = leadsData.total || 0;
  const maxLeads = leadsData.max_leads || 0;
  const isAtLimit = currentLeads >= maxLeads;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-pink-50 relative overflow-hidden">
      {/* Rich Animated background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-[800px] h-[800px] bg-gradient-to-br from-purple-400 via-pink-400 to-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob"></div>
        <div className="absolute top-1/4 -left-40 w-[700px] h-[700px] bg-gradient-to-br from-pink-400 via-rose-400 to-orange-300 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 right-1/4 w-[750px] h-[750px] bg-gradient-to-br from-blue-400 via-purple-400 to-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob animation-delay-4000"></div>
      </div>

      {/* Top Navigation */}
      <ResponsiveNav user={user} onLogout={handleLogout} />

      <div className="p-6 sm:p-8 max-w-[95%] mx-auto relative z-10">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <div className="flex items-center gap-4 mb-4">
            <Button
              onClick={() => navigate('/dashboard')}
              variant="outline"
              className="flex items-center gap-2 hover:bg-purple-50"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </Button>
          </div>
          
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center gap-3">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-400 to-amber-600 flex items-center justify-center shadow-lg">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                Leads Management
              </h1>
              <p className="text-lg text-gray-600">Manage and track your business leads</p>
            </div>
            
            {/* Leads Counter - Top Right */}
            <div className="bg-white rounded-xl px-6 py-4 shadow-md border border-gray-100">
              <p className="text-sm text-gray-600 mb-1">Leads Used</p>
              <p className="text-3xl font-bold text-purple-600">
                {currentLeads} / {maxLeads}
              </p>
              <p className="text-xs text-gray-500 mt-1">{planName}</p>
            </div>
          </div>
        </div>

        {/* Free User - Blurred Overlay */}
        {isFree && (
          <div className="relative">
            {/* Blurred Background Content */}
            <div className="filter blur-sm pointer-events-none select-none opacity-40">
              <div className="bg-white rounded-xl p-6 shadow-md border border-gray-100 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search leads..."
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg"
                      disabled
                    />
                  </div>
                  <Button disabled className="ml-4">
                    <Plus className="w-4 h-4 mr-2" />
                    Add New Lead
                  </Button>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gradient-to-r from-purple-50 to-pink-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Name</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Email</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Phone</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Company</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[1, 2, 3, 4, 5].map((i) => (
                      <tr key={i} className="border-t border-gray-100">
                        <td className="px-6 py-4 text-sm">John Doe {i}</td>
                        <td className="px-6 py-4 text-sm">john{i}@example.com</td>
                        <td className="px-6 py-4 text-sm">+1 234 567 890{i}</td>
                        <td className="px-6 py-4 text-sm">Company {i}</td>
                        <td className="px-6 py-4 text-sm">Active</td>
                        <td className="px-6 py-4 text-sm">
                          <Button size="sm" variant="outline" disabled>Edit</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Centered Upgrade Message Overlay */}
            <div className="absolute inset-0 flex items-center justify-center z-10">
              <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl border-2 border-purple-200 p-10 max-w-2xl mx-4 text-center transform hover:scale-105 transition-transform">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <Lock className="w-10 h-10 text-white" />
                </div>
                
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  🔒 Upgrade to unlock your leads!
                </h2>
                
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Get access to <span className="font-bold text-purple-600">100 leads</span> with the <span className="font-bold">Starter Plan</span> or{' '}
                  <span className="font-bold text-purple-600">500 leads</span> with the <span className="font-bold">Professional Plan</span>
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-200">
                    <p className="text-sm font-semibold text-gray-700 mb-1">Starter Plan</p>
                    <p className="text-2xl font-bold text-blue-600">100 Leads</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-200">
                    <p className="text-sm font-semibold text-gray-700 mb-1">Professional Plan</p>
                    <p className="text-2xl font-bold text-purple-600">500 Leads</p>
                  </div>
                </div>
                
                <Button 
                  onClick={() => navigate('/subscription')}
                  size="lg"
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
                >
                  <TrendingUp className="w-5 h-5 mr-2" />
                  Upgrade Now
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Starter and Professional Users - Normal View */}
        {!isFree && (
          <>
            {/* Search and Add Button */}
            <div className="bg-white rounded-xl p-4 shadow-md border border-gray-100 mb-6 animate-fade-in-up">
              <div className="flex flex-col md:flex-row gap-3 items-center">
                <div className="flex-1 relative w-full">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search leads by name, email, phone, or company..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>
                <Button
                  onClick={() => setShowAddModal(true)}
                  disabled={isAtLimit}
                  className={`${isAtLimit ? 'opacity-50 cursor-not-allowed' : ''} bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white`}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add New Lead
                </Button>
              </div>
              
              {/* Limit Warning for Starter users */}
              {isStarter && isAtLimit && (
                <div className="mt-4 bg-gradient-to-r from-yellow-50 to-orange-50 border border-orange-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    <strong>⚠️ Limit Reached:</strong> You have reached your lead limit of {maxLeads}.{' '}
                    <button 
                      onClick={() => navigate('/subscription')}
                      className="text-purple-600 hover:text-purple-700 font-semibold underline"
                    >
                      Upgrade to the Professional plan
                    </button>
                    {' '}to unlock 500 leads.
                  </p>
                </div>
              )}

              {/* Limit Warning for Professional users */}
              {isProfessional && isAtLimit && (
                <div className="mt-4 bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    <strong>⚠️ Limit Reached:</strong> You have reached your lead limit of {maxLeads}.{' '}
                    Please contact support for Enterprise plan options.
                  </p>
                </div>
              )}
            </div>

            {/* Leads Table */}
            <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden animate-fade-in-up">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gradient-to-r from-purple-50 to-pink-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Name</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Email</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Phone</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Company</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Date Added</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {loading ? (
                      <tr>
                        <td colSpan="7" className="px-6 py-12 text-center text-gray-500">
                          <div className="flex flex-col items-center">
                            <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mb-4"></div>
                            <p>Loading leads...</p>
                          </div>
                        </td>
                      </tr>
                    ) : filteredLeads.length === 0 ? (
                      <tr>
                        <td colSpan="7" className="px-6 py-12 text-center">
                          <div className="flex flex-col items-center justify-center text-gray-500">
                            <FileText className="w-16 h-16 text-gray-300 mb-4" />
                            <p className="text-lg font-semibold mb-2">No Leads Yet</p>
                            <p className="text-sm">Click "Add New Lead" to get started</p>
                          </div>
                        </td>
                      </tr>
                    ) : (
                      filteredLeads.map((lead) => (
                        <tr key={lead.id} className="border-t border-gray-100 hover:bg-purple-50 transition-colors">
                          <td className="px-6 py-4 text-sm font-medium text-gray-900">{lead.name || 'N/A'}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">{lead.email || 'N/A'}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">{lead.phone || 'N/A'}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">{lead.company || 'N/A'}</td>
                          <td className="px-6 py-4">
                            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                              lead.status === 'active' ? 'bg-green-100 text-green-800' :
                              lead.status === 'contacted' ? 'bg-blue-100 text-blue-800' :
                              lead.status === 'converted' ? 'bg-purple-100 text-purple-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {lead.status || 'active'}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-600">
                            {lead.created_at ? new Date(lead.created_at).toLocaleDateString() : 'N/A'}
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex gap-2">
                              <Button 
                                size="sm" 
                                variant="outline"
                                onClick={() => handleEditClick(lead)}
                                className="text-blue-600 hover:bg-blue-50"
                              >
                                <Edit className="w-4 h-4" />
                              </Button>
                              <Button 
                                size="sm" 
                                variant="outline"
                                onClick={() => handleDeleteLead(lead.id)}
                                className="text-red-600 hover:bg-red-50"
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Info Card for Plan Limits */}
            <div className="mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 animate-fade-in-up">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-500 flex items-center justify-center flex-shrink-0">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Your Plan: {planName}</h4>
                  <p className="text-sm text-gray-600">
                    You have <strong className="text-purple-600">{currentLeads} out of {maxLeads}</strong> leads used
                    {' '}({Math.round((currentLeads / maxLeads) * 100)}% used)
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {isStarter && !isAtLimit && 'Want more leads? Upgrade to Professional for 500 leads'}
                    {isProfessional && !isAtLimit && 'You have access to all Professional features (500 leads)'}
                    {isAtLimit && isStarter && '⚠️ Limit reached - Upgrade to Professional for more leads'}
                    {isAtLimit && isProfessional && '⚠️ Limit reached - Contact support for Enterprise plan'}
                  </p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Add Lead Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between sticky top-0 bg-white">
              <h3 className="text-2xl font-bold text-gray-900">Add New Lead</h3>
              <button 
                onClick={() => setShowAddModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="john@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="+1 234 567 8900"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company</label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => setFormData({...formData, company: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Acme Corp"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="active">Active</option>
                  <option value="contacted">Contacted</option>
                  <option value="converted">Converted</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Additional notes about this lead..."
                />
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex gap-3 justify-end sticky bottom-0 bg-white">
              <Button 
                variant="outline" 
                onClick={() => setShowAddModal(false)}
              >
                Cancel
              </Button>
              <Button 
                onClick={handleAddLead}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
              >
                Add Lead
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Lead Modal */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between sticky top-0 bg-white">
              <h3 className="text-2xl font-bold text-gray-900">Edit Lead</h3>
              <button 
                onClick={() => setShowEditModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="john@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="+1 234 567 8900"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company</label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => setFormData({...formData, company: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Acme Corp"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="active">Active</option>
                  <option value="contacted">Contacted</option>
                  <option value="converted">Converted</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Additional notes about this lead..."
                />
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex gap-3 justify-end sticky bottom-0 bg-white">
              <Button 
                variant="outline" 
                onClick={() => setShowEditModal(false)}
              >
                Cancel
              </Button>
              <Button 
                onClick={handleUpdateLead}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
              >
                Update Lead
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leads;
