import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, MessageSquare, Star, Clock, RefreshCw } from 'lucide-react';
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || ''
});

const AdvancedAnalytics = ({ chatbotId }) => {
  const [loading, setLoading] = useState(false);
  const [period, setPeriod] = useState('7days');
  const [trendData, setTrendData] = useState(null);
  const [topQuestions, setTopQuestions] = useState(null);
  const [satisfaction, setSatisfaction] = useState(null);
  const [performance, setPerformance] = useState(null);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const [trends, questions, sat, perf] = await Promise.all([
        api.get(`/api/analytics/trends/${chatbotId}?period=${period}`).then(r => r.data),
        api.get(`/api/analytics/top-questions/${chatbotId}`).then(r => r.data),
        api.get(`/api/analytics/satisfaction/${chatbotId}`).then(r => r.data),
        api.get(`/api/analytics/performance/${chatbotId}`).then(r => r.data),
      ]);
      
      setTrendData(trends);
      setTopQuestions(questions);
      setSatisfaction(sat);
      setPerformance(perf);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, [chatbotId, period]);

  const COLORS = ['#7c3aed', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'];

  const satisfactionPieData = satisfaction ? [
    { name: '5 Stars', value: satisfaction.rating_distribution[5] },
    { name: '4 Stars', value: satisfaction.rating_distribution[4] },
    { name: '3 Stars', value: satisfaction.rating_distribution[3] },
    { name: '2 Stars', value: satisfaction.rating_distribution[2] },
    { name: '1 Star', value: satisfaction.rating_distribution[1] },
  ].filter(item => item.value > 0) : [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Period Selector */}
      <div className="flex justify-between items-center">
        <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          Advanced Analytics
        </h3>
        <div className="flex space-x-2">
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          >
            <option value="7days">Last 7 Days</option>
            <option value="30days">Last 30 Days</option>
            <option value="90days">Last 90 Days</option>
          </select>
          <button
            onClick={loadAnalytics}
            className="p-2 bg-purple-100 text-purple-600 rounded-lg hover:bg-purple-200 transition-colors"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm mb-1">Avg Daily Messages</p>
              <p className="text-3xl font-bold">{trendData?.avg_daily_messages?.toFixed(1) || 0}</p>
            </div>
            <TrendingUp className="w-8 h-8 text-purple-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-pink-100 text-sm mb-1">Total Conversations</p>
              <p className="text-3xl font-bold">{trendData?.total_conversations || 0}</p>
            </div>
            <MessageSquare className="w-8 h-8 text-pink-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-indigo-100 text-sm mb-1">Satisfaction Rate</p>
              <p className="text-3xl font-bold">{satisfaction?.satisfaction_percentage?.toFixed(1) || 0}%</p>
            </div>
            <Star className="w-8 h-8 text-indigo-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm mb-1">Avg Response Time</p>
              <p className="text-3xl font-bold">{(performance?.avg_response_time_ms / 1000)?.toFixed(1) || 0}s</p>
            </div>
            <Clock className="w-8 h-8 text-blue-200" />
          </div>
        </div>
      </div>

      {/* Message Trends Chart */}
      {trendData && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h4 className="text-lg font-semibold mb-4">Message Volume Trends</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" stroke="#888" fontSize={12} />
              <YAxis stroke="#888" fontSize={12} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="conversations" 
                stroke="#7c3aed" 
                strokeWidth={2}
                name="Conversations"
                dot={{ fill: '#7c3aed' }}
              />
              <Line 
                type="monotone" 
                dataKey="messages" 
                stroke="#ec4899" 
                strokeWidth={2}
                name="Messages"
                dot={{ fill: '#ec4899' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Top Questions Chart */}
        {topQuestions && topQuestions.top_questions.length > 0 && (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h4 className="text-lg font-semibold mb-4">Top Asked Questions</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topQuestions.top_questions.slice(0, 5)}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="question" stroke="#888" fontSize={10} angle={-15} textAnchor="end" height={80} />
                <YAxis stroke="#888" fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="count" fill="#7c3aed" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Satisfaction Distribution Chart */}
        {satisfaction && satisfactionPieData.length > 0 && (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h4 className="text-lg font-semibold mb-4">Satisfaction Distribution</h4>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={satisfactionPieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {satisfactionPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                Average Rating: <span className="font-bold text-purple-600">{satisfaction.average_rating.toFixed(1)}/5.0</span>
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Based on {satisfaction.total_ratings} ratings
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Performance Metrics */}
      {performance && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h4 className="text-lg font-semibold mb-4">Performance Metrics</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Fastest Response</p>
              <p className="text-2xl font-bold text-purple-600">
                {(performance.fastest_response_ms / 1000).toFixed(2)}s
              </p>
            </div>
            <div className="p-4 bg-pink-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Average Response</p>
              <p className="text-2xl font-bold text-pink-600">
                {(performance.avg_response_time_ms / 1000).toFixed(2)}s
              </p>
            </div>
            <div className="p-4 bg-indigo-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Slowest Response</p>
              <p className="text-2xl font-bold text-indigo-600">
                {(performance.slowest_response_ms / 1000).toFixed(2)}s
              </p>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-4 text-center">
            Total Responses: {performance.total_responses}
          </p>
        </div>
      )}
    </div>
  );
};

export default AdvancedAnalytics;
