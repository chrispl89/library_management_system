import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Books from './Books';
import { AuthProvider } from '../context/AuthContext';
import api from '../services/api';

jest.mock('../services/api');

const MockedBooks = () => (
  <BrowserRouter>
    <AuthProvider>
      <Books />
    </AuthProvider>
  </BrowserRouter>
);

describe('Books Component', () => {
  const mockBooks = [
    {
      id: 1,
      title: 'Test Book 1',
      author: 'Author 1',
      category: 'Fiction',
      is_available: true,
      added_by: 1
    },
    {
      id: 2,
      title: 'Test Book 2',
      author: 'Author 2',
      category: 'Science',
      is_available: false,
      added_by: 1
    }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('displays loading state initially', () => {
    api.get.mockImplementation(() => new Promise(() => {}));
    
    render(<MockedBooks />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('renders books list after loading', async () => {
    api.get.mockResolvedValue({ data: mockBooks });
    
    render(<MockedBooks />);
    
    await waitFor(() => {
      expect(screen.getByText('Test Book 1')).toBeInTheDocument();
      expect(screen.getByText('Test Book 2')).toBeInTheDocument();
    });
  });

  test('displays available status correctly', async () => {
    api.get.mockResolvedValue({ data: mockBooks });
    
    render(<MockedBooks />);
    
    await waitFor(() => {
      const availableBadges = screen.getAllByText(/available/i);
      expect(availableBadges.length).toBeGreaterThan(0);
    });
  });

  test('shows error message on API failure', async () => {
    api.get.mockRejectedValue(new Error('API Error'));
    
    render(<MockedBooks />);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('displays empty state when no books', async () => {
    api.get.mockResolvedValue({ data: [] });
    
    render(<MockedBooks />);
    
    await waitFor(() => {
      expect(screen.getByText(/no books/i)).toBeInTheDocument();
    });
  });
});
