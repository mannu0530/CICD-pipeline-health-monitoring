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
  Chip,
  IconButton,
  Tooltip,
  Alert,
  Snackbar,
  LinearProgress,
  Pagination,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Settings as SettingsIcon,
  GitHub as GitHubIcon,
  Build as BuildIcon,
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Code as CodeIcon,
} from '@mui/icons-material';

interface ConfigItem {
  id: string;
  name: string;
  type: string;
  category: string;
  description: string;
  status: string;
  environment: string;
  lastModified: string;
  modifiedBy: string;
}

const Configuration: React.FC = () => {
  const [configs, setConfigs] = useState<ConfigItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterText, setFilterText] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
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
      setConfigs([
        {
          id: 'config-1',
          name: 'GitHub Actions Integration',
          type: 'integration',
          category: 'CI/CD',
          description: 'Configuration for GitHub Actions webhook integration',
          status: 'active',
          environment: 'production',
          lastModified: '2024-01-15T09:00:00Z',
          modifiedBy: 'admin@example.com',
        },
        {
          id: 'config-2',
          name: 'Slack Notifications',
          type: 'notification',
          category: 'Alerts',
          description: 'Slack webhook configuration for pipeline notifications',
          status: 'active',
          environment: 'production',
          lastModified: '2024-01-15T08:30:00Z',
          modifiedBy: 'devops@example.com',
        },
        {
          id: 'config-3',
          name: 'Build Environment Settings',
          type: 'build',
          category: 'Infrastructure',
          description: 'Build environment configuration including resource limits and timeouts',
          status: 'active',
          environment: 'production',
          lastModified: '2024-01-15T08:00:00Z',
          modifiedBy: 'admin@example.com',
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'pipeline':
        return 'primary';
      case 'build':
        return 'secondary';
      case 'notification':
        return 'info';
      case 'security':
        return 'warning';
      case 'integration':
        return 'success';
      default:
        return 'default';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'pipeline':
        return <CodeIcon />;
      case 'build':
        return <BuildIcon />;
      case 'notification':
        return <NotificationsIcon />;
      case 'security':
        return <SecurityIcon />;
      case 'integration':
        return <GitHubIcon />;
      default:
        return <SettingsIcon />;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const handleCreateConfig = () => {
    setSnackbar({
      open: true,
      message: 'New configuration functionality coming soon!',
      severity: 'info',
    });
  };

  const filteredConfigs = configs.filter(config => {
    const matchesText = config.name.toLowerCase().includes(filterText.toLowerCase()) ||
                       config.description.toLowerCase().includes(filterText.toLowerCase());
    const matchesType = typeFilter === 'all' || config.type === typeFilter;
    
    return matchesText && matchesType;
  });

  const paginatedConfigs = filteredConfigs.slice(
    (page - 1) * rowsPerPage,
    page * rowsPerPage
  );

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading configuration...
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
            Configuration Management
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Manage system configuration, integrations, and settings
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateConfig}
          size="large"
        >
          New Configuration
        </Button>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab label="Configuration Items" />
          <Tab label="Integrations" />
          <Tab label="System Settings" />
        </Tabs>
      </Box>

      {activeTab === 0 && (
        <>
          {/* Filters */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={3} alignItems="center">
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Search Configurations"
                    value={filterText}
                    onChange={(e) => setFilterText(e.target.value)}
                    placeholder="Search by name, description, or category..."
                    InputProps={{
                      startAdornment: <FilterIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                    }}
                  />
                </Grid>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Type</InputLabel>
                    <Select
                      value={typeFilter}
                      label="Type"
                      onChange={(e) => setTypeFilter(e.target.value)}
                    >
                      <MenuItem value="all">All Types</MenuItem>
                      <MenuItem value="pipeline">Pipeline</MenuItem>
                      <MenuItem value="build">Build</MenuItem>
                      <MenuItem value="notification">Notification</MenuItem>
                      <MenuItem value="security">Security</MenuItem>
                      <MenuItem value="integration">Integration</MenuItem>
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
                      setTypeFilter('all');
                    }}
                  >
                    Reset
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Configuration Table */}
          <Card>
            <CardContent>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Configuration</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Category</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Environment</TableCell>
                      <TableCell>Last Modified</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {paginatedConfigs.map((config) => (
                      <TableRow key={config.id} hover>
                        <TableCell>
                          <Box>
                            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                              {config.name}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" sx={{ maxWidth: 300 }}>
                              {config.description}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip
                            icon={getTypeIcon(config.type)}
                            label={config.type}
                            color={getTypeColor(config.type) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {config.category}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={config.status}
                            color={config.status === 'active' ? 'success' : 'default'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={config.environment}
                            size="small"
                            variant="outlined"
                            color="primary"
                          />
                        </TableCell>
                        <TableCell>
                          <Box>
                            <Typography variant="body2">
                              {formatTimestamp(config.lastModified)}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                              by {config.modifiedBy}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', gap: 0.5 }}>
                            <Tooltip title="Edit Configuration">
                              <IconButton
                                size="small"
                                color="primary"
                                onClick={() => setSnackbar({ open: true, message: 'Edit functionality coming soon!', severity: 'info' })}
                              >
                                <EditIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Delete Configuration">
                              <IconButton
                                size="small"
                                color="error"
                                onClick={() => setSnackbar({ open: true, message: 'Delete functionality coming soon!', severity: 'info' })}
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
                  count={Math.ceil(filteredConfigs.length / rowsPerPage)}
                  page={page}
                  onChange={(_, value) => setPage(value)}
                  color="primary"
                />
              </Box>
            </CardContent>
          </Card>
        </>
      )}

      {activeTab === 1 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              Integration Status
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Integration management interface coming soon...
            </Typography>
          </CardContent>
        </Card>
      )}

      {activeTab === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              System Settings
            </Typography>
            <Typography variant="body2" color="textSecondary">
              System-level configuration and settings will be available here.
            </Typography>
          </CardContent>
        </Card>
      )}

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

export default Configuration;
