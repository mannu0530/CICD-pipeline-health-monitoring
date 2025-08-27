import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tooltip,
  Alert,
  Snackbar,
  LinearProgress,
  Pagination,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  PlayArrow as RunIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Build as BuildIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  PlayArrow as RunningIcon,
  Schedule as PendingIcon,
  Timeline as TimelineIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';

interface Build {
  id: string;
  pipelineId: string;
  pipelineName: string;
  status: 'success' | 'failure' | 'running' | 'pending' | 'cancelled';
  stage: string;
  startedAt: string;
  completedAt?: string;
  duration?: number;
  environment: string;
  branch: string;
  commit: string;
  commitMessage: string;
  triggerType: 'push' | 'pr' | 'manual' | 'schedule';
  triggeredBy: string;
  tests: {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
  };
  coverage: number;
}

const Builds: React.FC = () => {
  const [builds, setBuilds] = useState<Build[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedBuild, setSelectedBuild] = useState<Build | null>(null);
  const [buildDialogOpen, setBuildDialogOpen] = useState(false);
  const [filterText, setFilterText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [stageFilter, setStageFilter] = useState<string>('all');
  const [page, setPage] = useState(1);
  const [rowsPerPage] = useState(10);
  const [activeTab, setActiveTab] = useState(0);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' | 'info' | 'warning' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  // Mock data for demonstration
  useEffect(() => {
    setTimeout(() => {
      setBuilds([
        {
          id: 'build-1',
          pipelineId: '1',
          pipelineName: 'main-pipeline',
          status: 'success',
          stage: 'deploy',
          startedAt: '2024-01-15T10:30:00Z',
          completedAt: '2024-01-15T10:35:00Z',
          duration: 5.2,
          environment: 'production',
          branch: 'main',
          commit: 'a1b2c3d4e5f6',
          commitMessage: 'feat: Add new authentication system',
          triggerType: 'push',
          triggeredBy: 'john.doe@example.com',
          tests: { total: 156, passed: 156, failed: 0, skipped: 0 },
          coverage: 89.5,
        },
        {
          id: 'build-2',
          pipelineId: '2',
          pipelineName: 'feature-pipeline',
          status: 'running',
          stage: 'test',
          startedAt: '2024-01-15T10:25:00Z',
          environment: 'staging',
          branch: 'feature/auth',
          commit: 'b2c3d4e5f6g7',
          commitMessage: 'feat: Implement OAuth2 flow',
          triggerType: 'pr',
          triggeredBy: 'jane.smith@example.com',
          tests: { total: 89, passed: 45, failed: 0, skipped: 0 },
          coverage: 0,
        },
        {
          id: 'build-3',
          pipelineId: '3',
          pipelineName: 'deploy-pipeline',
          status: 'failure',
          stage: 'deploy',
          startedAt: '2024-01-15T10:20:00Z',
          completedAt: '2024-01-15T10:32:00Z',
          duration: 12.1,
          environment: 'production',
          branch: 'main',
          commit: 'c3d4e5f6g7h8',
          commitMessage: 'feat: Add monitoring infrastructure',
          triggerType: 'manual',
          triggeredBy: 'admin@example.com',
          tests: { total: 0, passed: 0, failed: 0, skipped: 0 },
          coverage: 0,
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'success';
      case 'failure':
        return 'error';
      case 'running':
        return 'info';
      case 'pending':
        return 'warning';
      case 'cancelled':
        return 'default';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <SuccessIcon />;
      case 'failure':
        return <ErrorIcon />;
      case 'running':
        return <RunningIcon />;
      case 'pending':
        return <PendingIcon />;
      case 'cancelled':
        return <TimelineIcon />;
      default:
        return <TimelineIcon />;
    }
  };

  const formatDuration = (minutes: number) => {
    if (minutes < 60) {
      return `${minutes.toFixed(1)}m`;
    }
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}h ${remainingMinutes.toFixed(0)}m`;
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const handleViewBuild = (build: Build) => {
    setSelectedBuild(build);
    setBuildDialogOpen(true);
  };

  const handleRerunBuild = (build: Build) => {
    setSnackbar({
      open: true,
      message: `Build ${build.id} restarted successfully`,
      severity: 'success',
    });
  };

  const handleStopBuild = (build: Build) => {
    setSnackbar({
      open: true,
      message: `Build ${build.id} stopped successfully`,
      severity: 'success',
    });
  };

  const filteredBuilds = builds.filter(build => {
    const matchesText = build.id.toLowerCase().includes(filterText.toLowerCase()) ||
                       build.pipelineName.toLowerCase().includes(filterText.toLowerCase()) ||
                       build.commitMessage.toLowerCase().includes(filterText.toLowerCase());
    const matchesStatus = statusFilter === 'all' || build.status === statusFilter;
    const matchesStage = stageFilter === 'all' || build.stage === stageFilter;
    return matchesText && matchesStatus && matchesStage;
  });

  const paginatedBuilds = filteredBuilds.slice(
    (page - 1) * rowsPerPage,
    page * rowsPerPage
  );

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading builds...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            Build Management
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Monitor and manage your CI/CD builds
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setSnackbar({ open: true, message: 'New build functionality coming soon!', severity: 'info' })}
          size="large"
        >
          New Build
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Search Builds"
                value={filterText}
                onChange={(e) => setFilterText(e.target.value)}
                placeholder="Search by ID, pipeline, or commit message..."
                InputProps={{
                  startAdornment: <FilterIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  label="Status"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="all">All Statuses</MenuItem>
                  <MenuItem value="success">Success</MenuItem>
                  <MenuItem value="failure">Failure</MenuItem>
                  <MenuItem value="running">Running</MenuItem>
                  <MenuItem value="pending">Pending</MenuItem>
                  <MenuItem value="cancelled">Cancelled</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Stage</InputLabel>
                <Select
                  value={stageFilter}
                  label="Stage"
                  onChange={(e) => setStageFilter(e.target.value)}
                >
                  <MenuItem value="all">All Stages</MenuItem>
                  <MenuItem value="build">Build</MenuItem>
                  <MenuItem value="test">Test</MenuItem>
                  <MenuItem value="deploy">Deploy</MenuItem>
                  <MenuItem value="validate">Validate</MenuItem>
                  <MenuItem value="plan">Plan</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={() => {
                  setFilterText('');
                  setStatusFilter('all');
                  setStageFilter('all');
                }}
              >
                Reset
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Builds Table */}
      <Card>
        <CardContent>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Build</TableCell>
                  <TableCell>Pipeline</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Stage</TableCell>
                  <TableCell>Duration</TableCell>
                  <TableCell>Tests</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedBuilds.map((build) => (
                  <TableRow key={build.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', fontFamily: 'monospace' }}>
                          {build.id}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{ maxWidth: 200 }}>
                          {build.commitMessage}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                          <Chip
                            label={build.environment}
                            size="small"
                            variant="outlined"
                            color="primary"
                          />
                          <Typography variant="caption" sx={{ ml: 1 }}>
                            {build.branch}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                        {build.pipelineName}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {build.triggerType} • {build.triggeredBy}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        icon={getStatusIcon(build.status)}
                        label={build.status}
                        color={getStatusColor(build.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={build.stage}
                        size="small"
                        variant="outlined"
                        color="primary"
                      />
                    </TableCell>
                    <TableCell>
                      {build.duration ? (
                        <Typography variant="body2">
                          {formatDuration(build.duration)}
                        </Typography>
                      ) : build.status === 'running' ? (
                        <Typography variant="body2" color="primary.main">
                          Running...
                        </Typography>
                      ) : (
                        <Typography variant="body2" color="textSecondary">
                          -
                        </Typography>
                      )}
                      <Typography variant="caption" color="textSecondary" display="block">
                        {formatTimestamp(build.startedAt)}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {build.tests.total > 0 ? (
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            {build.tests.passed}/{build.tests.total}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {build.coverage > 0 ? `${build.coverage}% coverage` : 'No coverage data'}
                          </Typography>
                        </Box>
                      ) : (
                        <Typography variant="body2" color="textSecondary">
                          No tests
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        <Tooltip title="View Details">
                          <IconButton
                            size="small"
                            onClick={() => handleViewBuild(build)}
                          >
                            <ViewIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        {build.status === 'running' ? (
                          <Tooltip title="Stop Build">
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => handleStopBuild(build)}
                            >
                              <StopIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        ) : (
                          <Tooltip title="Rerun Build">
                            <IconButton
                              size="small"
                              color="primary"
                              onClick={() => handleRerunBuild(build)}
                            >
                              <RunIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          {/* Pagination */}
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <Pagination
              count={Math.ceil(filteredBuilds.length / rowsPerPage)}
              page={page}
              onChange={(_, value) => setPage(value)}
              color="primary"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Build Details Dialog */}
      <Dialog
        open={buildDialogOpen}
        onClose={() => setBuildDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedBuild && (
          <>
            <DialogTitle>
              Build Details: {selectedBuild.id}
              <Typography variant="subtitle2" color="textSecondary">
                {selectedBuild.pipelineName} • {selectedBuild.commitMessage}
              </Typography>
            </DialogTitle>
            <DialogContent>
              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
                <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
                  <Tab label="Overview" />
                  <Tab label="Tests" />
                </Tabs>
              </Box>

              {activeTab === 0 && (
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>Build Information</Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Status</Typography>
                      <Chip
                        icon={getStatusIcon(selectedBuild.status)}
                        label={selectedBuild.status}
                        color={getStatusColor(selectedBuild.status) as any}
                        sx={{ mt: 0.5 }}
                      />
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Current Stage</Typography>
                      <Typography variant="body1">{selectedBuild.stage}</Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Environment</Typography>
                      <Typography variant="body1">{selectedBuild.environment}</Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Branch</Typography>
                      <Typography variant="body1">{selectedBuild.branch}</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>Timing & Metrics</Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Started At</Typography>
                      <Typography variant="body1">{formatTimestamp(selectedBuild.startedAt)}</Typography>
                    </Box>
                    {selectedBuild.completedAt && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" color="textSecondary">Completed At</Typography>
                        <Typography variant="body1">{formatTimestamp(selectedBuild.completedAt)}</Typography>
                      </Box>
                    )}
                    {selectedBuild.duration && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" color="textSecondary">Duration</Typography>
                        <Typography variant="body1">{formatDuration(selectedBuild.duration)}</Typography>
                      </Box>
                    )}
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Trigger</Typography>
                      <Typography variant="body1">{selectedBuild.triggerType} by {selectedBuild.triggeredBy}</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>Commit Information</Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                        {selectedBuild.commit}
                      </Typography>
                      <Typography variant="body1">
                        {selectedBuild.commitMessage}
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              )}

              {activeTab === 1 && (
                <Box>
                  <Typography variant="h6" gutterBottom>Test Results</Typography>
                  {selectedBuild.tests.total > 0 ? (
                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <Card>
                          <CardContent>
                            <Typography variant="h4" color="success.main" gutterBottom>
                              {selectedBuild.tests.passed}/{selectedBuild.tests.total}
                            </Typography>
                            <Typography variant="subtitle1">Tests Passed</Typography>
                            <Typography variant="body2" color="textSecondary">
                              {((selectedBuild.tests.passed / selectedBuild.tests.total) * 100).toFixed(1)}% success rate
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <Card>
                          <CardContent>
                            <Typography variant="h4" color="primary.main" gutterBottom>
                              {selectedBuild.coverage}%
                            </Typography>
                            <Typography variant="subtitle1">Code Coverage</Typography>
                            <Typography variant="body2" color="textSecondary">
                              {selectedBuild.tests.failed > 0 ? `${selectedBuild.tests.failed} tests failed` : 'All tests passed'}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    </Grid>
                  ) : (
                    <Typography variant="body2" color="textSecondary">
                      No test data available for this build.
                    </Typography>
                  )}
                </Box>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setBuildDialogOpen(false)}>Close</Button>
              {selectedBuild.status === 'running' ? (
                <Button
                  color="error"
                  variant="contained"
                  startIcon={<StopIcon />}
                  onClick={() => {
                    handleStopBuild(selectedBuild);
                    setBuildDialogOpen(false);
                  }}
                >
                  Stop Build
                </Button>
              ) : (
                <Button
                  color="primary"
                  variant="contained"
                  startIcon={<RunIcon />}
                  onClick={() => {
                    handleRerunBuild(selectedBuild);
                    setBuildDialogOpen(false);
                  }}
                >
                  Rerun Build
                </Button>
              )}
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Builds;
