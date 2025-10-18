import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BookOpen, BookMarked, Calendar, Star, ArrowRight } from 'lucide-react';

const Home = () => {
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: BookOpen,
      title: 'Browse Books',
      description: 'Explore our extensive collection of books across various categories',
      link: '/books',
      color: 'blue',
    },
    {
      icon: BookMarked,
      title: 'Manage Loans',
      description: 'Borrow books and track your reading progress',
      link: '/loans',
      color: 'green',
      auth: true,
    },
    {
      icon: Calendar,
      title: 'Reserve Books',
      description: 'Reserve books that are currently unavailable',
      link: '/reservations',
      color: 'purple',
      auth: true,
    },
    {
      icon: Star,
      title: 'Write Reviews',
      description: 'Share your thoughts and rate books you have read',
      link: '/reviews',
      color: 'yellow',
      auth: true,
    },
  ];

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-600',
      green: 'bg-green-100 text-green-600',
      purple: 'bg-purple-100 text-purple-600',
      yellow: 'bg-yellow-100 text-yellow-600',
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-6">
        <div className="flex justify-center">
          <BookOpen className="h-20 w-20 text-blue-600" />
        </div>
        <h1 className="text-5xl font-bold text-gray-900">
          Welcome to Library Management System
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Your digital gateway to managing books, loans, reservations, and reviews all in one place
        </p>
        
        {!isAuthenticated && (
          <div className="flex justify-center space-x-4">
            <Link
              to="/register"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="px-6 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
            >
              Sign In
            </Link>
          </div>
        )}
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon;
          const shouldShow = !feature.auth || isAuthenticated;
          
          if (!shouldShow) return null;

          return (
            <Link
              key={feature.title}
              to={feature.link}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow group"
            >
              <div className={`inline-flex p-3 rounded-lg ${getColorClasses(feature.color)} mb-4`}>
                <Icon className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                {feature.description}
              </p>
              <div className="flex items-center text-blue-600 text-sm font-medium group-hover:translate-x-1 transition-transform">
                <span>Learn more</span>
                <ArrowRight className="h-4 w-4 ml-1" />
              </div>
            </Link>
          );
        })}
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg shadow-xl p-8 text-white">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <p className="text-4xl font-bold mb-2">1000+</p>
            <p className="text-blue-100">Books Available</p>
          </div>
          <div>
            <p className="text-4xl font-bold mb-2">500+</p>
            <p className="text-blue-100">Active Members</p>
          </div>
          <div>
            <p className="text-4xl font-bold mb-2">24/7</p>
            <p className="text-blue-100">Online Access</p>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-blue-100 text-blue-600 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              1
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Create Account
            </h3>
            <p className="text-gray-600">
              Sign up for free and activate your account via email
            </p>
          </div>
          <div className="text-center">
            <div className="bg-green-100 text-green-600 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              2
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Browse & Borrow
            </h3>
            <p className="text-gray-600">
              Explore our collection and borrow books you like
            </p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 text-purple-600 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              3
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Read & Review
            </h3>
            <p className="text-gray-600">
              Enjoy your books and share your thoughts with others
            </p>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      {!isAuthenticated && (
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to get started?
          </h2>
          <p className="text-gray-600 mb-6">
            Join our community of book lovers today
          </p>
          <Link
            to="/register"
            className="inline-flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            <span>Create Free Account</span>
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      )}
    </div>
  );
};

export default Home;
