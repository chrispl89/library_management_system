import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import { AuthProvider } from '../context/AuthContext';

const MockedLayout = ({ children }) => (
  <BrowserRouter>
    <AuthProvider>
      <Layout>{children}</Layout>
    </AuthProvider>
  </BrowserRouter>
);

describe('Layout Component', () => {
  test('renders children content', () => {
    render(
      <MockedLayout>
        <div>Test Content</div>
      </MockedLayout>
    );
    
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  test('displays navigation links when authenticated', () => {
    render(
      <MockedLayout>
        <div>Content</div>
      </MockedLayout>
    );
    
    // Navigation should be present
    expect(screen.getByRole('navigation')).toBeInTheDocument();
  });

  test('renders footer', () => {
    render(
      <MockedLayout>
        <div>Content</div>
      </MockedLayout>
    );
    
    // Footer should be present
    const footer = screen.getByRole('contentinfo');
    expect(footer).toBeInTheDocument();
  });
});
