import React, { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import { User, BookMarked, Calendar, Star, AlertCircle } from 'lucide-react';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await dashboardAPI.get();
      setDashboardData(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4 flex items-center space-x-3">
        <AlertCircle className="h-5 w-5 text-red-600" />
        <span className="text-red-700">{error}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Loans</p>
              <p className="text-3xl font-bold text-blue-600">
                {dashboardData?.active_loans?.length || 0}
              </p>
            </div>
            <BookMarked className="h-12 w-12 text-blue-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Reservations</p>
              <p className="text-3xl font-bold text-green-600">
                {dashboardData?.active_reservations?.length || 0}
              </p>
            </div>
            <Calendar className="h-12 w-12 text-green-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Reviews</p>
              <p className="text-3xl font-bold text-yellow-600">
                {dashboardData?.reviews?.length || 0}
              </p>
            </div>
            <Star className="h-12 w-12 text-yellow-600 opacity-20" />
          </div>
        </div>
      </div>

      {/* Profile Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center space-x-3 mb-6">
          <User className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-bold text-gray-900">Profile Information</h2>
        </div>
        
        {dashboardData?.profile && (
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Username</p>
                <p className="font-medium text-gray-900">{dashboardData.profile.user_username}</p>
              </div>
              {dashboardData.profile.phone_number && (
                <div>
                  <p className="text-sm text-gray-600">Phone Number</p>
                  <p className="font-medium text-gray-900">{dashboardData.profile.phone_number}</p>
                </div>
              )}
              {dashboardData.profile.address && (
                <div className="md:col-span-2">
                  <p className="text-sm text-gray-600">Address</p>
                  <p className="font-medium text-gray-900">{dashboardData.profile.address}</p>
                </div>
              )}
            </div>
            
            {dashboardData.profile.activity_history && (
              <div className="mt-4 pt-4 border-t">
                <p className="text-sm text-gray-600 mb-2">Activity History</p>
                <div className="bg-gray-50 rounded-md p-3 max-h-40 overflow-y-auto">
                  <pre className="text-xs text-gray-700 whitespace-pre-wrap">
                    {dashboardData.profile.activity_history}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Active Loans */}
      {dashboardData?.active_loans && dashboardData.active_loans.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center space-x-3 mb-6">
            <BookMarked className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-bold text-gray-900">Active Loans</h2>
          </div>
          
          <div className="space-y-3">
            {dashboardData.active_loans.map((loan) => (
              <div key={loan.id} className="border rounded-md p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{loan.book_title}</p>
                    <p className="text-sm text-gray-600">Due: {new Date(loan.due_date).toLocaleDateString()}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    loan.status === 'OVERDUE' 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {loan.status}
                  </span>
                </div>
                {parseFloat(loan.fine) > 0 && (
                  <p className="text-sm text-red-600 mt-2">Fine: ${parseFloat(loan.fine).toFixed(2)}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Active Reservations */}
      {dashboardData?.active_reservations && dashboardData.active_reservations.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center space-x-3 mb-6">
            <Calendar className="h-6 w-6 text-green-600" />
            <h2 className="text-xl font-bold text-gray-900">Active Reservations</h2>
          </div>
          
          <div className="space-y-3">
            {dashboardData.active_reservations.map((reservation) => (
              <div key={reservation.id} className="border rounded-md p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{reservation.book_title}</p>
                    <p className="text-sm text-gray-600">
                      Expires: {new Date(reservation.expires_at).toLocaleDateString()}
                    </p>
                  </div>
                  <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                    {reservation.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Reviews */}
      {dashboardData?.reviews && dashboardData.reviews.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center space-x-3 mb-6">
            <Star className="h-6 w-6 text-yellow-600" />
            <h2 className="text-xl font-bold text-gray-900">My Reviews</h2>
          </div>
          
          <div className="space-y-3">
            {dashboardData.reviews.map((review) => (
              <div key={review.id} className="border rounded-md p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-medium text-gray-900">Book ID: {review.book}</p>
                  <div className="flex space-x-1">
                    {[...Array(review.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                    ))}
                  </div>
                </div>
                {review.comment && (
                  <p className="text-sm text-gray-600">{review.comment}</p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  {new Date(review.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
