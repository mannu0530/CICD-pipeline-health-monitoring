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
  Badge,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Notifications as NotificationsIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  CheckCircle as SuccessIcon,
  CheckCircleOutline as AcknowledgedIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

interface AlertItem {
  id: string;
  type: 'error' | 'warning' | 'info' | 'success';
  message: string;
  description: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  acknowledged: boolean;
  acknowledgedBy?: string;
  acknowledgedAt?: string;
  source: 'pipeline' | 'build' | 'system' | 'security' | 'deployment';
  sourceId: string;
  sourceName: string;
  environment: string;
  tags: string[];
}

const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAlert, setSelectedAlert] = useState<AlertItem | null>(null);
  const [alertDialogOpen, setAlertDialogOpen] = useState(false);
  const [filterText, setFilterText] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [severityFilter, setSeverityFilter] = useState<string>('all');
  const [sourceFilter, setSourceFilter] = useState<string>('all');
  const [acknowledgedFilter, setAcknowledgedFilter] = useState<string>('all');
  const [page, setPage] = useState(1);
  const [rowsPerPage] = useState(10);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' | 'info' | 'warning' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  // Mock data for demonstration
  useEffect(() => {
    setTimeout(() => {
      setAlerts([
        {
          id: 'alert-1',
          type: 'error',
          message: 'Pipeline main-pipeline failed at deploy stage',
          description: 'The deployment stage failed due to insufficient permissions in the production environment.',
          timestamp: '2024-01-15T10:20:00Z',
          severity: 'high',
          acknowledged: false,
          source: 'pipeline',
          sourceId: 'pipeline-1',
          sourceName: 'main-pipeline',
          environment: 'production',
          tags: ['deployment', 'permissions', 'rbac'],
        },
        {
          id: 'alert-2',
          type: 'warning',
          message: 'High memory usage detected in build environment',
          description: 'The build environment is experiencing high memory usage (85%+) which may impact build performance.',
          timestamp: '2024-01-15T10:15:00Z',
          severity: 'medium',
          acknowledged: true,
          acknowledgedBy: 'john.doe@example.com',
          acknowledgedAt: '2024-01-15T10:18:00Z',
          source: 'system',
          sourceId: 'build-node-1',
          sourceName: 'Build Node 1',
          environment: 'staging',
          tags: ['performance', 'memory', 'infrastructure'],
        },
        {
          id: 'alert-3',
          type: 'info',
          message: 'New security patch available for Jenkins',
          description: 'A critical security patch (CVE-2024-1234) is available for Jenkins.',
          timestamp: '2024-01-15T10:10:00Z',
          severity: 'low',
          acknowledged: false,
          source: 'security',
          sourceId: 'jenkins-instance',
          sourceName: 'Jenkins CI Server',
          environment: 'production',
          tags: ['security', 'jenkins', 'cve', 'patch'],
        },
        {
          id: 'alert-4',
          type: 'success',
          message: 'Pipeline feature-pipeline completed successfully',
          description: 'The feature branch pipeline completed all stages successfully.',
          timestamp: '2024-01-15T10:05:00Z',
          severity: 'low',
          acknowledged: false,
          source: 'pipeline',
          sourceId: 'pipeline-2',
          sourceName: 'feature-pipeline',
          environment: 'staging',
          tags: ['success', 'feature', 'staging'],
        },
        {
          id: 'alert-5',
          type: 'error',
          message: 'Database connection timeout in production',
          description: 'The application is experiencing database connection timeouts in production.',
          timestamp: '2024-01-15T10:00:00Z',
          severity: 'critical',
          acknowledged: false,
          source: 'system',
          sourceId: 'db-cluster-1',
          sourceName: 'Database Cluster',
          environment: 'production',
          tags: ['database', 'timeout', 'critical', 'production'],
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'error':
        return 'error';
      case 'warning':
        return 'warning';
      case 'info':
        return 'info';
      case 'success':
        return 'success';
      default:
        return 'default';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'error':
        return <ErrorIcon />;
      case 'warning':
        return <WarningIcon />;
      case 'info':
        return <InfoIcon />;
      case 'success':
        return <SuccessIcon />;
      default:
        return <InfoIcon />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return '#d32f2f';
      case 'high':
        return '#f44336';
      case 'medium':
        return '#ff9800';
      case 'low':
        return '#2196f3';
      default:
        return '#757575';
    }
  };

  const getSeverityLabel = (severity: string) => {
    return severity.charAt(0).toUpperCase() + severity.slice(1);
  };

  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'pipeline':
        return <SettingsIcon />;
      case 'build':
        return <SettingsIcon />;
      case 'system':
        return <SettingsIcon />;
      case 'security':
        return <WarningIcon />;
      case 'deployment':
        return <SettingsIcon />;
      default:
        return <InfoIcon />;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const handleViewAlert = (alert: AlertItem) => {
    setSelectedAlert(alert);
    setAlertDialogOpen(true);
  };

  const handleAcknowledgeAlert = (alert: AlertItem) => {
    const updatedAlert = {
      ...alert,
      acknowledged: true,
      acknowledgedBy: 'current-user@example.com',
      acknowledgedAt: new Date().toISOString(),
    };
    
    setAlerts(alerts.map(a => a.id === alert.id ? updatedAlert : a));
    setSnackbar({
      open: true,
      message: `Alert "${alert.message}" acknowledged successfully`,
      severity: 'success',
    });
  };

  const handleDeleteAlert = (alert: AlertItem) => {
    if (window.confirm(`Are you sure you want to delete alert "${alert.message}"?`)) {
      setAlerts(alerts.filter(a => a.id !== alert.id));
      setSnackbar({
        open: true,
        message: `Alert "${alert.message}" deleted successfully`,
        severity: 'success',
      });
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    const matchesText = alert.message.toLowerCase().includes(filterText.toLowerCase()) ||
                       alert.description.toLowerCase().includes(filterText.toLowerCase()) ||
                       alert.sourceName.toLowerCase().includes(filterText.toLowerCase());
    const matchesType = typeFilter === 'all' || alert.type === typeFilter;
    const matchesSeverity = severityFilter === 'all' || alert.severity === severityFilter;
    const matchesSource = sourceFilter === 'all' || alert.source === sourceFilter;
    const matchesAcknowledged = acknowledgedFilter === 'all' || 
                                (acknowledgedFilter === 'acknowledged' && alert.acknowledged) ||
                                (acknowledgedFilter === 'unacknowledged' && !alert.acknowledged);
    
    return matchesText && matchesType && matchesSeverity && matchesSource && matchesAcknowledged;
  });

  const paginatedAlerts = filteredAlerts.slice(
    (page - 1) * rowsPerPage,
    page * rowsPerPage
  );

  const unacknowledgedCount = alerts.filter(a => !a.acknowledged).length;
  const criticalCount = alerts.filter(a => a.severity === 'critical' && !a.acknowledged).length;

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading alerts...
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
            Alert Management
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Monitor and manage system alerts and notifications
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Badge badgeContent={unacknowledgedCount} color="error" sx={{ mr: 1 }}>
            <NotificationsIcon color="action" />
          </Badge>
          {criticalCount > 0 && (
            <Chip
              label={`${criticalCount} Critical`}
              color="error"
              variant="filled"
              size="small"
            />
          )}
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setSnackbar({ open: true, message: 'New alert functionality coming soon!', severity: 'info' })}
            size="large"
          >
            New Alert
          </Button>
        </Box>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Search Alerts"
                value={filterText}
                onChange={(e) => setFilterText(e.target.value)}
                placeholder="Search by message, description, or source..."
                InputProps={{
                  startAdornment: <FilterIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Type</InputLabel>
                <Select
                  value={typeFilter}
                  label="Type"
                  onChange={(e) => setTypeFilter(e.target.value)}
                >
                  <MenuItem value="all">All Types</MenuItem>
                  <MenuItem value="error">Error</MenuItem>
                  <MenuItem value="warning">Warning</MenuItem>
                  <MenuItem value="info">Info</MenuItem>
                  <MenuItem value="success">Success</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Severity</InputLabel>
                <Select
                  value={severityFilter}
                  label="Severity"
                  onChange={(e) => setSeverityFilter(e.target.value)}
                >
                  <MenuItem value="all">All Severities</MenuItem>
                  <MenuItem value="critical">Critical</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Source</InputLabel>
                <Select
                  value={sourceFilter}
                  label="Source"
                  onChange={(e) => setSourceFilter(e.target.value)}
                >
                  <MenuItem value="all">All Sources</MenuItem>
                  <MenuItem value="pipeline">Pipeline</MenuItem>
                  <MenuItem value="build">Build</MenuItem>
                  <MenuItem value="system">System</MenuItem>
                  <MenuItem value="security">Security</MenuItem>
                  <MenuItem value="deployment">Deployment</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={acknowledgedFilter}
                  label="Status"
                  onChange={(e) => setAcknowledgedFilter(e.target.value)}
                >
                  <MenuItem value="all">All Statuses</MenuItem>
                  <MenuItem value="unacknowledged">Unacknowledged</MenuItem>
                  <MenuItem value="acknowledged">Acknowledged</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={1}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={() => {
                  setFilterText('');
                  setTypeFilter('all');
                  setSeverityFilter('all');
                  setSourceFilter('all');
                  setAcknowledgedFilter('all');
                }}
              >
                Reset
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Alerts Table */}
      <Card>
        <CardContent>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Alert</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Severity</TableCell>
                  <TableCell>Source</TableCell>
                  <TableCell>Environment</TableCell>
                  <TableCell>Timestamp</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedAlerts.map((alert) => (
                  <TableRow key={alert.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                          {alert.message}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{ maxWidth: 300 }}>
                          {alert.description}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 0.5, mt: 1 }}>
                          {alert.tags.map((tag) => (
                            <Chip
                              key={tag}
                              label={tag}
                              size="small"
                              variant="outlined"
                              sx={{ fontSize: '0.7rem' }}
                            />
                          ))}
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        icon={getTypeIcon(alert.type)}
                        label={alert.type}
                        color={getTypeColor(alert.type) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={getSeverityLabel(alert.severity)}
                        size="small"
                        sx={{
                          bgcolor: getSeverityColor(alert.severity),
                          color: 'white',
                          fontWeight: 'bold'
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getSourceIcon(alert.source)}
                        <Typography variant="body2">
                          {alert.sourceName}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={alert.environment}
                        size="small"
                        variant="outlined"
                        color="primary"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {formatTimestamp(alert.timestamp)}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {alert.acknowledged ? (
                        <Chip
                          icon={<AcknowledgedIcon />}
                          label="Acknowledged"
                          color="success"
                          size="small"
                        />
                      ) : (
                        <Chip
                          icon={<WarningIcon />}
                          label="Unacknowledged"
                          color="warning"
                          size="small"
                        />
                      )}
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        <Tooltip title="View Details">
                          <IconButton
                            size="small"
                            onClick={() => handleViewAlert(alert)}
                          >
                            <ViewIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        {!alert.acknowledged && (
                          <Tooltip title="Acknowledge">
                            <IconButton
                              size="small"
                              color="success"
                              onClick={() => handleAcknowledgeAlert(alert)}
                            >
                              <AcknowledgedIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                        <Tooltip title="Delete">
                          <IconButton
                            size="small"
                            color="error"
                            onClick={() => handleDeleteAlert(alert)}
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
              count={Math.ceil(filteredAlerts.length / rowsPerPage)}
              page={page}
              onChange={(_, value) => setPage(value)}
              color="primary"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Alert Details Dialog */}
      <Dialog
        open={alertDialogOpen}
        onClose={() => setAlertDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedAlert && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                {getTypeIcon(selectedAlert.type)}
                <Box>
                  <Typography variant="h6">
                    Alert Details
                  </Typography>
                  <Typography variant="subtitle2" color="textSecondary">
                    {selectedAlert.sourceName} • {selectedAlert.environment}
                  </Typography>
                </Box>
              </Box>
            </DialogTitle>
            <DialogContent>
              <Grid container spacing={3} sx={{ mt: 1 }}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>Message</Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {selectedAlert.message}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {selectedAlert.description}
                  </Typography>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>Alert Information</Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Type</Typography>
                    <Chip
                      icon={getTypeIcon(selectedAlert.type)}
                      label={selectedAlert.type}
                      color={getTypeColor(selectedAlert.type) as any}
                      sx={{ mt: 0.5 }}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Severity</Typography>
                    <Chip
                      label={getSeverityLabel(selectedAlert.severity)}
                      sx={{
                        bgcolor: getSeverityColor(selectedAlert.severity),
                        color: 'white',
                        fontWeight: 'bold',
                        mt: 0.5
                      }}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Timestamp</Typography>
                    <Typography variant="body2">
                      {formatTimestamp(selectedAlert.timestamp)}
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Tags</Typography>
                    <Box sx={{ display: 'flex', gap: 0.5, mt: 0.5, flexWrap: 'wrap' }}>
                      {selectedAlert.tags.map((tag) => (
                        <Chip
                          key={tag}
                          label={tag}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>Source Information</Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Source Type</Typography>
                    <Typography variant="body2">
                      {selectedAlert.source}
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Source Name</Typography>
                    <Typography variant="body2">
                      {selectedAlert.sourceName}
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">Environment</Typography>
                    <Typography variant="body2">
                      {selectedAlert.environment}
                    </Typography>
                  </Box>
                  {selectedAlert.acknowledged && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">Acknowledged By</Typography>
                      <Typography variant="body2">
                        {selectedAlert.acknowledgedBy} at {selectedAlert.acknowledgedAt && formatTimestamp(selectedAlert.acknowledgedAt)}
                      </Typography>
                    </Box>
                  )}
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setAlertDialogOpen(false)}>Close</Button>
              {!selectedAlert.acknowledged && (
                <Button
                  color="success"
                  variant="contained"
                  startIcon={<AcknowledgedIcon />}
                  onClick={() => {
                    handleAcknowledgeAlert(selectedAlert);
                    setAlertDialogOpen(false);
                  }}
                >
                  Acknowledge
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

export default Alerts;
