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
  Fab,
  Alert,
  Snackbar,
  LinearProgress,
  Pagination,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  PlayArrow as RunIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Code as CodeIcon,
  Settings as SettingsIcon,
  GitHub as GitHubIcon,
  Build as BuildIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  PlayArrow as RunningIcon,
  Schedule as PendingIcon,
} from '@mui/icons-material';

interface Pipeline {
  id: string;
  name: string;
  description: string;
  repository: string;
  branch: string;
  status: 'active' | 'inactive' | 'draft';
  triggerType: 'push' | 'pr' | 'manual' | 'schedule';
  lastRun?: string;
  lastStatus?: 'success' | 'failure' | 'running' | 'pending';
  averageDuration?: number;
  successRate: number;
  totalRuns: number;
  environment: string;
  createdAt: string;
}

const Pipelines: React.FC = () => {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPipeline, setEditingPipeline] = useState<Pipeline | null>(null);
  const [filterText, setFilterText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [page, setPage] = useState(1);
  const [rowsPerPage] = useState(10);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  // Mock data for demonstration
  useEffect(() => {
    setTimeout(() => {
      setPipelines([
        {
          id: '1',
          name: 'main-pipeline',
          description: 'Main CI/CD pipeline for the application',
          repository: 'myapp/frontend',
          branch: 'main',
          status: 'active',
          triggerType: 'push',
          lastRun: '2024-01-15T10:30:00Z',
          lastStatus: 'success',
          averageDuration: 5.2,
          successRate: 92.5,
          totalRuns: 156,
          environment: 'production',
          createdAt: '2024-01-01T00:00:00Z',
        },
        {
          id: '2',
          name: 'feature-pipeline',
          description: 'Pipeline for feature branch testing',
          repository: 'myapp/backend',
          branch: 'feature/*',
          status: 'active',
          triggerType: 'pr',
          lastRun: '2024-01-15T10:25:00Z',
          lastStatus: 'running',
          averageDuration: 8.1,
          successRate: 87.3,
          totalRuns: 89,
          environment: 'staging',
          createdAt: '2024-01-05T00:00:00Z',
        },
        {
          id: '3',
          name: 'deploy-pipeline',
          description: 'Production deployment pipeline',
          repository: 'myapp/infrastructure',
          branch: 'main',
          status: 'active',
          triggerType: 'manual',
          lastRun: '2024-01-15T10:20:00Z',
          lastStatus: 'failure',
          averageDuration: 12.5,
          successRate: 78.9,
          totalRuns: 45,
          environment: 'production',
          createdAt: '2024-01-10T00:00:00Z',
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'default';
      case 'draft':
        return 'warning';
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
      default:
        return <PendingIcon />;
    }
  };

  const getTriggerIcon = (triggerType: string) => {
    switch (triggerType) {
      case 'push':
        return <GitHubIcon />;
      case 'pr':
        return <CodeIcon />;
      case 'manual':
        return <SettingsIcon />;
      case 'schedule':
        return <PendingIcon />;
      default:
        return <PendingIcon />;
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

  const handleCreatePipeline = () => {
    setEditingPipeline({
      id: '',
      name: '',
      description: '',
      repository: '',
      branch: '',
      status: 'draft',
      triggerType: 'push',
      successRate: 0,
      totalRuns: 0,
      environment: 'staging',
      createdAt: new Date().toISOString(),
    });
    setDialogOpen(true);
  };

  const handleEditPipeline = (pipeline: Pipeline) => {
    setEditingPipeline({ ...pipeline });
    setDialogOpen(true);
  };

  const handleDeletePipeline = (pipeline: Pipeline) => {
    if (window.confirm(`Are you sure you want to delete pipeline "${pipeline.name}"?`)) {
      setPipelines(pipelines.filter(p => p.id !== pipeline.id));
      setSnackbar({
        open: true,
        message: `Pipeline "${pipeline.name}" deleted successfully`,
        severity: 'success',
      });
    }
  };

  const handleRunPipeline = (pipeline: Pipeline) => {
    setSnackbar({
      open: true,
      message: `Pipeline "${pipeline.name}" started successfully`,
      severity: 'success',
    });
  };

  const handleSavePipeline = () => {
    if (editingPipeline) {
      if (editingPipeline.id) {
        // Update existing pipeline
        setPipelines(pipelines.map(p => 
          p.id === editingPipeline.id ? { ...editingPipeline } : p
        ));
        setSnackbar({
          open: true,
          message: `Pipeline "${editingPipeline.name}" updated successfully`,
          severity: 'success',
        });
      } else {
        // Create new pipeline
        const newPipeline = { ...editingPipeline, id: Date.now().toString() };
        setPipelines([...pipelines, newPipeline]);
        setSnackbar({
          open: true,
          message: `Pipeline "${newPipeline.name}" created successfully`,
          severity: 'success',
        });
      }
      setDialogOpen(false);
      setEditingPipeline(null);
    }
  };

  const filteredPipelines = pipelines.filter(pipeline => {
    const matchesText = pipeline.name.toLowerCase().includes(filterText.toLowerCase()) ||
                       pipeline.description.toLowerCase().includes(filterText.toLowerCase()) ||
                       pipeline.repository.toLowerCase().includes(filterText.toLowerCase());
    const matchesStatus = statusFilter === 'all' || pipeline.status === statusFilter;
    return matchesText && matchesStatus;
  });

  const paginatedPipelines = filteredPipelines.slice(
    (page - 1) * rowsPerPage,
    page * rowsPerPage
  );

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading pipelines...
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
            Pipeline Management
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Manage and monitor your CI/CD pipelines
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreatePipeline}
          size="large"
        >
          Create Pipeline
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Search Pipelines"
                value={filterText}
                onChange={(e) => setFilterText(e.target.value)}
                placeholder="Search by name, description, or repository..."
                InputProps={{
                  startAdornment: <FilterIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  label="Status"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="all">All Statuses</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="inactive">Inactive</MenuItem>
                  <MenuItem value="draft">Draft</MenuItem>
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
                }}
              >
                Reset
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Pipelines Table */}
      <Card>
        <CardContent>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Pipeline</TableCell>
                  <TableCell>Repository</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Trigger</TableCell>
                  <TableCell>Last Run</TableCell>
                  <TableCell>Success Rate</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedPipelines.map((pipeline) => (
                  <TableRow key={pipeline.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                          {pipeline.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{ maxWidth: 200 }}>
                          {pipeline.description}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                          <Chip
                            label={pipeline.environment}
                            size="small"
                            variant="outlined"
                            color="primary"
                          />
                          <Typography variant="caption" sx={{ ml: 1 }}>
                            {pipeline.branch}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                        {pipeline.repository}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={pipeline.status}
                        color={getStatusColor(pipeline.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Tooltip title={pipeline.triggerType}>
                        <IconButton size="small">
                          {getTriggerIcon(pipeline.triggerType)}
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                    <TableCell>
                      {pipeline.lastRun ? (
                        <Box>
                          <Typography variant="body2">
                            {formatTimestamp(pipeline.lastRun)}
                          </Typography>
                          {pipeline.lastStatus && (
                            <Chip
                              icon={getStatusIcon(pipeline.lastStatus)}
                              label={pipeline.lastStatus}
                              color={pipeline.lastStatus === 'success' ? 'success' : 
                                     pipeline.lastStatus === 'failure' ? 'error' : 
                                     pipeline.lastStatus === 'running' ? 'info' : 'warning'}
                              size="small"
                              sx={{ mt: 0.5 }}
                            />
                          )}
                        </Box>
                      ) : (
                        <Typography variant="body2" color="textSecondary">
                          Never run
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell>
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                          {pipeline.successRate.toFixed(1)}%
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {pipeline.totalRuns} runs
                        </Typography>
                        {pipeline.averageDuration && (
                          <Typography variant="caption" color="textSecondary" display="block">
                            Avg: {formatDuration(pipeline.averageDuration)}
                          </Typography>
                        )}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        <Tooltip title="Run Pipeline">
                          <IconButton
                            size="small"
                            color="primary"
                            onClick={() => handleRunPipeline(pipeline)}
                          >
                            <RunIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit Pipeline">
                          <IconButton
                            size="small"
                            color="primary"
                            onClick={() => handleEditPipeline(pipeline)}
                          >
                            <EditIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete Pipeline">
                          <IconButton
                            size="small"
                            color="error"
                            onClick={() => handleDeletePipeline(pipeline)}
                          >
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
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
              count={Math.ceil(filteredPipelines.length / rowsPerPage)}
              page={page}
              onChange={(_, value) => setPage(value)}
              color="primary"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Create/Edit Pipeline Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => {
          setDialogOpen(false);
          setEditingPipeline(null);
        }}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editingPipeline?.id ? 'Edit Pipeline' : 'Create New Pipeline'}
        </DialogTitle>
        <DialogContent>
          {editingPipeline && (
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Pipeline Name"
                  value={editingPipeline.name}
                  onChange={(e) => setEditingPipeline({ ...editingPipeline, name: e.target.value })}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={editingPipeline.status}
                    label="Status"
                    onChange={(e) => setEditingPipeline({ ...editingPipeline, status: e.target.value as any })}
                  >
                    <MenuItem value="draft">Draft</MenuItem>
                    <MenuItem value="active">Active</MenuItem>
                    <MenuItem value="inactive">Inactive</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  value={editingPipeline.description}
                  onChange={(e) => setEditingPipeline({ ...editingPipeline, description: e.target.value })}
                  margin="normal"
                  multiline
                  rows={3}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Repository"
                  value={editingPipeline.repository}
                  onChange={(e) => setEditingPipeline({ ...editingPipeline, repository: e.target.value })}
                  margin="normal"
                  placeholder="owner/repository"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Branch"
                  value={editingPipeline.branch}
                  onChange={(e) => setEditingPipeline({ ...editingPipeline, branch: e.target.value })}
                  margin="normal"
                  placeholder="main"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Trigger Type</InputLabel>
                  <Select
                    value={editingPipeline.triggerType}
                    label="Trigger Type"
                    onChange={(e) => setEditingPipeline({ ...editingPipeline, triggerType: e.target.value as any })}
                  >
                    <MenuItem value="push">Push</MenuItem>
                    <MenuItem value="pr">Pull Request</MenuItem>
                    <MenuItem value="manual">Manual</MenuItem>
                    <MenuItem value="schedule">Schedule</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Environment"
                  value={editingPipeline.environment}
                  onChange={(e) => setEditingPipeline({ ...editingPipeline, environment: e.target.value })}
                  margin="normal"
                  placeholder="staging"
                />
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setDialogOpen(false);
            setEditingPipeline(null);
          }}>
            Cancel
          </Button>
          <Button
            color="primary"
            variant="contained"
            onClick={handleSavePipeline}
            disabled={!editingPipeline?.name || !editingPipeline?.repository}
          >
            {editingPipeline?.id ? 'Update' : 'Create'} Pipeline
          </Button>
        </DialogActions>
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

export default Pipelines;
