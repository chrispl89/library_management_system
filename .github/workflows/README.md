# GitHub Actions Workflows

## tests.yml - Automated Testing

This workflow runs comprehensive tests on every push and pull request to main/master/develop branches.

### Jobs:

#### 1. **django-tests** - Backend Testing
- Sets up PostgreSQL 15 database
- Installs Python 3.11 and dependencies
- Runs database migrations
- Executes 27 Django unit tests
- Tests API endpoints, permissions, and business logic

**Requirements:**
- PostgreSQL service must be healthy
- All dependencies in `django/requirements.txt` installed
- DATABASE_URL environment variable set

#### 2. **react-tests** - Frontend Testing
- Sets up Node.js 18
- Installs npm dependencies
- Runs Jest tests for React components
- Builds production bundle
- Tests UI components, forms, and routing

**Requirements:**
- Node.js 18+
- All dependencies in `frontend/package.json` installed
- Clean npm ci install with `--legacy-peer-deps`

#### 3. **docker-build** - Integration Testing
- Runs after django-tests and react-tests pass
- Builds Docker images for all services
- Starts full Docker Compose stack (PostgreSQL, Django, React, Nginx)
- Performs health checks on all services
- Creates test data (users and books)
- Runs Django tests inside Docker container
- Verifies production-like environment

**Services tested:**
- PostgreSQL database (port 5432)
- Django backend (port 8000)
- React frontend (port 3000)
- Nginx reverse proxy

### Test Results:

✅ **27 Django backend tests** covering:
- Book CRUD operations
- Loan lifecycle and fine calculation
- Reservation system
- Review management
- Statistics API
- Google Books integration
- User permissions
- Profile management

✅ **React component tests** covering:
- Login form and validation
- Book listing and search
- Dashboard display
- Layout and navigation

### Troubleshooting:

**PostgreSQL connection issues:**
- Ensure health check passes before running migrations
- Wait for `pg_isready` to return success
- Check DATABASE_URL format

**Django test failures:**
- Verify all dependencies are installed
- Check Python version (3.11 required)
- Ensure migrations run successfully

**React test failures:**
- Use `npm ci --legacy-peer-deps` for clean install
- Set `CI=true` environment variable
- Use `--watchAll=false --passWithNoTests --ci` flags

**Docker build issues:**
- Increase wait time for services to start
- Check health endpoints (backend: `/api/books/`, frontend: `/`)
- Review Docker Compose configuration
- Check container logs on failure

### Environment Variables:

**Django:**
- `DATABASE_URL` - PostgreSQL connection string
- `DJANGO_SECRET_KEY` - Secret key for testing
- `DJANGO_DEBUG` - Set to True for CI

**React:**
- `CI=true` - Enables CI mode for tests
- `REACT_APP_API_URL` - Backend API URL

### Caching:

The workflow uses GitHub Actions cache for:
- Python pip packages (`~/.cache/pip`)
- Node modules (`frontend/node_modules`)

This speeds up subsequent runs significantly.

### Manual Trigger:

You can manually trigger the workflow from GitHub Actions tab:
1. Go to Actions tab
2. Select "Tests" workflow
3. Click "Run workflow"
4. Choose branch
5. Click "Run workflow"

### Status Badge:

Add this to README.md to show test status:

```markdown
[![Tests](https://github.com/chrispl89/library_management_system/actions/workflows/tests.yml/badge.svg)](https://github.com/chrispl89/library_management_system/actions/workflows/tests.yml)
```
