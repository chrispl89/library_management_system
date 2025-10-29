import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from './Dashboard';
import { AuthProvider } from '../context/AuthContext';
import api from '../services/api';

jest.mock('../services/api');

const MockedDashboard = () => (
  <BrowserRouter>
    <AuthProvider>
      <Dashboard />
    </AuthProvider>
  </BrowserRouter>
);

describe('Dashboard Component', () => {
  const mockDashboardData = {
    profile: {
      user: 'testuser',
      phone_number: '123456789',
      address: '123 Test St'
    },
    active_loans: [
      {
        id: 1,
        book_title: 'Borrowed Book',
        due_date: '2025-12-31',
        status: 'ACTIVE'
      }
    ],
    active_reservations: [
      {
        id: 1,
        book_title: 'Reserved Book',
        expires_at: '2025-11-01',
        status: 'ACTIVE'
      }
    ],
    reviews: [
      {
        id: 1,
        book_title: 'Reviewed Book',
        rating: 5,
        comment: 'Great book!'
      }
    ]
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('displays loading state', () => {
    api.get.mockImplementation(() => new Promise(() => {}));
    
    render(<MockedDashboard />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('renders dashboard sections after loading', async () => {
    api.get.mockResolvedValue({ data: mockDashboardData });
    
    render(<MockedDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/active loans/i)).toBeInTheDocument();
      expect(screen.getByText(/reservations/i)).toBeInTheDocument();
      expect(screen.getByText(/reviews/i)).toBeInTheDocument();
    });
  });

  test('displays active loans information', async () => {
    api.get.mockResolvedValue({ data: mockDashboardData });
    
    render(<MockedDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Borrowed Book')).toBeInTheDocument();
    });
  });

  test('shows empty state when no data', async () => {
    const emptyData = {
      profile: {},
      active_loans: [],
      active_reservations: [],
      reviews: []
    };
    api.get.mockResolvedValue({ data: emptyData });
    
    render(<MockedDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/no active loans/i)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    api.get.mockRejectedValue(new Error('Failed to fetch'));
    
    render(<MockedDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
