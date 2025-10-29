import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { BarChart3, TrendingUp, Users, BookOpen, Clock, Star, AlertCircle } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      setLoading(true);
      const response = await api.get('/statistics/');
      setStats(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner size="lg" text="Loading statistics..." />;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4 flex items-center space-x-3">
        <AlertCircle className="h-5 w-5 text-red-600" />
        <span className="text-red-700">{error}</span>
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Library Statistics</h1>
        <button
          onClick={fetchStatistics}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={<BookOpen className="h-6 w-6" />}
          title="Total Books"
          value={stats.books_statistics.total}
          color="blue"
        />
        <StatCard
          icon={<BookOpen className="h-6 w-6" />}
          title="Available Books"
          value={stats.books_statistics.available}
          color="green"
        />
        <StatCard
          icon={<Clock className="h-6 w-6" />}
          title="Active Loans"
          value={stats.loans_statistics.by_status.active}
          color="yellow"
        />
        <StatCard
          icon={<AlertCircle className="h-6 w-6" />}
          title="Overdue Loans"
          value={stats.loans_statistics.overdue_count}
          color="red"
        />
      </div>

      {/* Most Borrowed Books */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="h-5 w-5 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">Most Borrowed Books</h2>
        </div>
        {stats.most_borrowed_books.length > 0 ? (
          <div className="space-y-3">
            {stats.most_borrowed_books.map((book, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{book.book__title}</p>
                  <p className="text-sm text-gray-600">by {book.book__author}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                    {book.loan_count} loans
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No loan data available</p>
        )}
      </div>

      {/* Most Active Users */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Users className="h-5 w-5 text-green-600" />
          <h2 className="text-xl font-semibold text-gray-900">Most Active Users</h2>
        </div>
        {stats.most_active_users.length > 0 ? (
          <div className="space-y-3">
            {stats.most_active_users.map((user, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center justify-center w-8 h-8 bg-green-100 text-green-800 rounded-full font-semibold">
                    {index + 1}
                  </div>
                  <p className="font-medium text-gray-900">{user.user__username}</p>
                </div>
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                  {user.loan_count} loans
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No user data available</p>
        )}
      </div>

      {/* Top Rated Books */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Star className="h-5 w-5 text-yellow-600" />
          <h2 className="text-xl font-semibold text-gray-900">Top Rated Books</h2>
        </div>
        {stats.top_rated_books.length > 0 ? (
          <div className="space-y-3">
            {stats.top_rated_books.map((book, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{book.book__title}</p>
                  <p className="text-sm text-gray-600">{book.review_count} reviews</p>
                </div>
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                  <span className="font-semibold text-gray-900">
                    {book.avg_rating.toFixed(1)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No rating data available</p>
        )}
      </div>

      {/* Categories Distribution */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-2 mb-4">
          <BarChart3 className="h-5 w-5 text-purple-600" />
          <h2 className="text-xl font-semibold text-gray-900">Categories Distribution</h2>
        </div>
        {stats.categories_distribution.length > 0 ? (
          <div className="space-y-3">
            {stats.categories_distribution.map((category, index) => {
              const percentage = (category.count / stats.books_statistics.total) * 100;
              return (
                <div key={index} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-gray-900">{category.category}</span>
                    <span className="text-gray-600">{category.count} books ({percentage.toFixed(1)}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-purple-600 h-2 rounded-full transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-gray-500">No category data available</p>
        )}
      </div>

      {/* Loan Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Loans by Status</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Active</span>
              <span className="font-semibold text-yellow-600">
                {stats.loans_statistics.by_status.active}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Returned</span>
              <span className="font-semibold text-green-600">
                {stats.loans_statistics.by_status.returned}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Overdue</span>
              <span className="font-semibold text-red-600">
                {stats.loans_statistics.by_status.overdue}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Loans (Last 30 Days)</span>
              <span className="font-semibold text-blue-600">
                {stats.loans_statistics.recent_loans_30_days}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Active Reservations</span>
              <span className="font-semibold text-purple-600">
                {stats.reservations_statistics.active}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Expired Reservations</span>
              <span className="font-semibold text-gray-600">
                {stats.reservations_statistics.expired}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, color }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    red: 'bg-red-100 text-red-600',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className={`inline-flex p-3 rounded-lg ${colorClasses[color]} mb-3`}>
        {icon}
      </div>
      <p className="text-sm text-gray-600 mb-1">{title}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );
};

export default Statistics;
