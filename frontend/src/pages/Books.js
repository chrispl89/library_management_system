import React, { useState, useEffect } from 'react';
import { booksAPI, loansAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { BookOpen, Plus, Edit, Trash2, Search, X, CheckCircle, AlertCircle, BookMarked, ArrowUpDown } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import { validateBookForm, hasErrors } from '../utils/validation';

const Books = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);
  const [googleBooks, setGoogleBooks] = useState([]);
  const [searchingGoogle, setSearchingGoogle] = useState(false);
  const [sortBy, setSortBy] = useState('title');
  const [sortOrder, setSortOrder] = useState('asc');
  const [validationErrors, setValidationErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const { user } = useAuth();

  const [formData, setFormData] = useState({
    title: '',
    author: '',
    category: '',
  });

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const response = await booksAPI.getAll();
      setBooks(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch books');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchGoogle = async () => {
    if (!searchQuery.trim()) return;
    
    try {
      setSearchingGoogle(true);
      const response = await booksAPI.searchGoogle(searchQuery);
      setGoogleBooks(response.data.items || []);
    } catch (err) {
      console.error('Google Books search failed:', err);
    } finally {
      setSearchingGoogle(false);
    }
  };

  const handleAddFromGoogle = (googleBook) => {
    const volumeInfo = googleBook.volumeInfo;
    setFormData({
      title: volumeInfo.title || '',
      author: volumeInfo.authors?.join(', ') || '',
      category: volumeInfo.categories?.join(', ') || '',
    });
    setGoogleBooks([]);
    setSearchQuery('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const errors = validateBookForm(formData);
    setValidationErrors(errors);
    
    if (hasErrors(errors)) {
      return;
    }
    
    try {
      setSubmitting(true);
      if (showEditModal && selectedBook) {
        await booksAPI.update(selectedBook.id, formData);
      } else {
        await booksAPI.create(formData);
      }
      fetchBooks();
      resetForm();
    } catch (err) {
      setError('Failed to save book');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this book?')) {
      try {
        await booksAPI.delete(id);
        fetchBooks();
      } catch (err) {
        setError('Failed to delete book');
        console.error(err);
      }
    }
  };

  const handleEdit = (book) => {
    setSelectedBook(book);
    setFormData({
      title: book.title,
      author: book.author,
      category: book.category,
    });
    setShowEditModal(true);
  };

  const resetForm = () => {
    setFormData({ title: '', author: '', category: '' });
    setShowAddModal(false);
    setShowEditModal(false);
    setSelectedBook(null);
    setGoogleBooks([]);
    setSearchQuery('');
    setValidationErrors({});
    setSubmitting(false);
  };

  const handleBorrow = async (book) => {
    if (!user) {
      setError('Please login to borrow books');
      return;
    }

    // Set due date to 14 days from now
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + 14);
    const dueDateString = dueDate.toISOString().split('T')[0];

    try {
      await loansAPI.create({
        book: book.id,
        due_date: dueDateString
      });
      setError('');
      alert(`Successfully borrowed "${book.title}"! Due date: ${dueDateString}`);
      fetchBooks(); // Refresh book list to update availability
    } catch (err) {
      setError(err.response?.data?.non_field_errors?.[0] || 'Failed to borrow book');
      console.error(err);
    }
  };

  const isLibrarian = user?.role === 'librarian' || user?.role === 'admin';

  // Get unique categories from books
  const categories = ['all', ...new Set(books.map(book => book.category).sort())];

  const filteredBooks = books
    .filter(book => {
      const matchesSearch = book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.category.toLowerCase().includes(searchQuery.toLowerCase());
      
      const matchesCategory = selectedCategory === 'all' || book.category === selectedCategory;
      
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      let aValue = a[sortBy];
      let bValue = b[sortBy];
      
      // Handle availability sorting
      if (sortBy === 'is_available') {
        aValue = a.is_available ? 1 : 0;
        bValue = b.is_available ? 1 : 0;
      }
      
      // String comparison
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
      } else {
        return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
      }
    });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Books</h1>
        {isLibrarian && (
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            <Plus className="h-5 w-5" />
            <span>Add Book</span>
          </button>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 flex items-center space-x-3">
          <AlertCircle className="h-5 w-5 text-red-600" />
          <span className="text-red-700">{error}</span>
        </div>
      )}

      {/* Search and Filters */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search books by title, author, or category..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div className="md:w-48">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white"
            >
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </option>
              ))}
            </select>
          </div>
          <div className="md:w-48">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 bg-white"
            >
              <option value="title">Sort by Title</option>
              <option value="author">Sort by Author</option>
              <option value="category">Sort by Category</option>
              <option value="is_available">Sort by Availability</option>
            </select>
          </div>
          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            title={`Sort ${sortOrder === 'asc' ? 'Descending' : 'Ascending'}`}
          >
            <ArrowUpDown className="h-5 w-5 text-gray-600" />
          </button>
        </div>
        <div className="mt-3 flex items-center justify-between">
          <span className="text-sm text-gray-600">
            Showing <strong>{filteredBooks.length}</strong> of <strong>{books.length}</strong> books
          </span>
          {(selectedCategory !== 'all' || searchQuery) && (
            <button
              onClick={() => {
                setSelectedCategory('all');
                setSearchQuery('');
              }}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              Clear all filters
            </button>
          )}
        </div>
      </div>

      {/* Books Grid */}
      {loading ? (
        <LoadingSpinner size="lg" text="Loading books..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBooks.map((book) => (
            <div key={book.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <BookOpen className="h-8 w-8 text-blue-600" />
                {book.is_available ? (
                  <span className="flex items-center space-x-1 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    <CheckCircle className="h-3 w-3" />
                    <span>Available</span>
                  </span>
                ) : (
                  <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                    Unavailable
                  </span>
                )}
              </div>
              
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{book.title}</h3>
              <p className="text-sm text-gray-600 mb-1">by {book.author}</p>
              <p className="text-sm text-gray-500 mb-3">Category: {book.category}</p>
              {isLibrarian && (
                <p className="text-xs text-gray-400">Added by: {book.added_by}</p>
              )}

              {/* Borrow button for all authenticated users */}
              {user && book.is_available && (
                <div className="mt-4 pt-4 border-t">
                  <button
                    onClick={() => handleBorrow(book)}
                    className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                  >
                    <BookMarked className="h-4 w-4" />
                    <span>Borrow Book</span>
                  </button>
                </div>
              )}

              {/* Edit/Delete buttons for librarians */}
              {isLibrarian && (
                <div className="flex space-x-2 mt-4 pt-4 border-t">
                  <button
                    onClick={() => handleEdit(book)}
                    className="flex-1 flex items-center justify-center space-x-1 px-3 py-2 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
                  >
                    <Edit className="h-4 w-4" />
                    <span>Edit</span>
                  </button>
                  <button
                    onClick={() => handleDelete(book.id)}
                    className="flex-1 flex items-center justify-center space-x-1 px-3 py-2 bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors"
                  >
                    <Trash2 className="h-4 w-4" />
                    <span>Delete</span>
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {filteredBooks.length === 0 && !loading && (
        <div className="text-center py-12 text-gray-500">
          No books found
        </div>
      )}

      {/* Add/Edit Modal */}
      {(showAddModal || showEditModal) && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  {showEditModal ? 'Edit Book' : 'Add New Book'}
                </h2>
                <button onClick={resetForm} className="text-gray-400 hover:text-gray-600">
                  <X className="h-6 w-6" />
                </button>
              </div>

              {showAddModal && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Search Google Books
                  </label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSearchGoogle()}
                      placeholder="Search for books..."
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    />
                    <button
                      onClick={handleSearchGoogle}
                      disabled={searchingGoogle}
                      className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                    >
                      {searchingGoogle ? 'Searching...' : 'Search'}
                    </button>
                  </div>

                  {googleBooks.length > 0 && (
                    <div className="mt-4 space-y-2 max-h-60 overflow-y-auto">
                      {googleBooks.map((book, index) => (
                        <div
                          key={index}
                          onClick={() => handleAddFromGoogle(book)}
                          className="p-3 border rounded-md hover:bg-gray-50 cursor-pointer"
                        >
                          <p className="font-medium">{book.volumeInfo.title}</p>
                          <p className="text-sm text-gray-600">
                            {book.volumeInfo.authors?.join(', ')}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => {
                      setFormData({ ...formData, title: e.target.value });
                      if (validationErrors.title) {
                        setValidationErrors({ ...validationErrors, title: null });
                      }
                    }}
                    className={`w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500 ${
                      validationErrors.title ? 'border-red-500' : 'border-gray-300'
                    }`}
                  />
                  {validationErrors.title && (
                    <p className="mt-1 text-sm text-red-600">{validationErrors.title}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Author <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.author}
                    onChange={(e) => {
                      setFormData({ ...formData, author: e.target.value });
                      if (validationErrors.author) {
                        setValidationErrors({ ...validationErrors, author: null });
                      }
                    }}
                    className={`w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500 ${
                      validationErrors.author ? 'border-red-500' : 'border-gray-300'
                    }`}
                  />
                  {validationErrors.author && (
                    <p className="mt-1 text-sm text-red-600">{validationErrors.author}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Category <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.category}
                    onChange={(e) => {
                      setFormData({ ...formData, category: e.target.value });
                      if (validationErrors.category) {
                        setValidationErrors({ ...validationErrors, category: null });
                      }
                    }}
                    className={`w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500 ${
                      validationErrors.category ? 'border-red-500' : 'border-gray-300'
                    }`}
                  />
                  {validationErrors.category && (
                    <p className="mt-1 text-sm text-red-600">{validationErrors.category}</p>
                  )}
                </div>

                <div className="flex space-x-3 pt-4">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {submitting ? 'Saving...' : (showEditModal ? 'Update Book' : 'Add Book')}
                  </button>
                  <button
                    type="button"
                    onClick={resetForm}
                    disabled={submitting}
                    className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors disabled:opacity-50"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Books;
