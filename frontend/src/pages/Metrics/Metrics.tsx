import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Speed as SpeedIcon,
  Build as BuildIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Schedule as PendingIcon,
  PlayArrow as RunningIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  ComposedChart,
} from 'recharts';

interface MetricsData {
  timeRange: string;
  totalPipelines: number;
  totalBuilds: number;
  successRate: number;
  failureRate: number;
  averageBuildTime: number;
  averagePipelineTime: number;
  totalDeployments: number;
  deploymentSuccessRate: number;
  codeCoverage: number;
  testPassRate: number;
  trends: TrendData[];
  topPipelines: TopPipeline[];
  buildDistribution: BuildDistribution[];
  timeMetrics: TimeMetric[];
}

interface TrendData {
  date: string;
  success: number;
  failure: number;
  running: number;
  pending: number;
  buildTime: number;
  pipelineTime: number;
}

interface TopPipeline {
  name: string;
  successRate: number;
  totalRuns: number;
  averageTime: number;
  lastRun: string;
  status: string;
}

interface BuildDistribution {
  stage: string;
  count: number;
  successRate: number;
  averageTime: number;
}

interface TimeMetric {
  metric: string;
  current: number;
  previous: number;
  change: number;
  trend: 'up' | 'down' | 'stable';
}

const Metrics: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d');
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' | 'info' | 'warning' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  // Mock data for demonstration
  useEffect(() => {
    setTimeout(() => {
      setMetrics({
        timeRange: '7d',
        totalPipelines: 156,
        totalBuilds: 1247,
        successRate: 87.2,
        failureRate: 12.8,
        averageBuildTime: 8.5,
        averagePipelineTime: 15.2,
        totalDeployments: 89,
        deploymentSuccessRate: 94.4,
        codeCoverage: 78.9,
        testPassRate: 92.1,
        trends: [
          { date: 'Jan 9', success: 12, failure: 2, running: 1, pending: 0, buildTime: 7.2, pipelineTime: 13.5 },
          { date: 'Jan 10', success: 15, failure: 1, running: 2, pending: 1, buildTime: 6.8, pipelineTime: 12.8 },
          { date: 'Jan 11', success: 18, failure: 3, running: 1, pending: 0, buildTime: 8.1, pipelineTime: 14.2 },
          { date: 'Jan 12', success: 14, failure: 2, running: 3, pending: 1, buildTime: 7.9, pipelineTime: 15.8 },
          { date: 'Jan 13', success: 16, failure: 1, running: 2, pending: 0, buildTime: 8.3, pipelineTime: 16.1 },
          { date: 'Jan 14', success: 20, failure: 2, running: 1, pending: 1, buildTime: 7.7, pipelineTime: 14.9 },
          { date: 'Jan 15', success: 17, failure: 1, running: 3, pending: 0, buildTime: 8.5, pipelineTime: 15.2 },
        ],
        topPipelines: [
          { name: 'main-pipeline', successRate: 95.2, totalRuns: 156, averageTime: 12.3, lastRun: '2024-01-15T10:30:00Z', status: 'success' },
          { name: 'feature-pipeline', successRate: 87.3, totalRuns: 89, averageTime: 8.1, lastRun: '2024-01-15T10:25:00Z', status: 'running' },
          { name: 'deploy-pipeline', successRate: 78.9, totalRuns: 45, averageTime: 18.5, lastRun: '2024-01-15T10:20:00Z', status: 'failure' },
          { name: 'test-pipeline', successRate: 91.7, totalRuns: 67, averageTime: 5.2, lastRun: '2024-01-15T10:15:00Z', status: 'success' },
        ],
        buildDistribution: [
          { stage: 'Build', count: 1247, successRate: 89.2, averageTime: 3.2 },
          { stage: 'Test', count: 1247, successRate: 87.1, averageTime: 5.8 },
          { stage: 'Deploy', count: 1247, successRate: 84.3, averageTime: 8.5 },
          { stage: 'Validate', count: 1247, successRate: 92.7, averageTime: 1.5 },
        ],
        timeMetrics: [
          { metric: 'Build Time', current: 8.5, previous: 9.2, change: -7.6, trend: 'down' },
          { metric: 'Pipeline Time', current: 15.2, previous: 16.8, change: -9.5, trend: 'down' },
          { metric: 'Success Rate', current: 87.2, previous: 85.1, change: 2.5, trend: 'up' },
          { metric: 'Code Coverage', current: 78.9, previous: 76.2, change: 3.5, trend: 'up' },
        ],
      });
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

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon color="success" />;
      case 'down':
        return <TrendingDownIcon color="error" />;
      default:
        return <TrendingDownIcon color="info" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'success.main';
      case 'down':
        return 'error.main';
      default:
        return 'text.secondary';
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

  const handleRefresh = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSnackbar({
        open: true,
        message: 'Metrics refreshed successfully',
        severity: 'success',
      });
    }, 1000);
  };

  const handleExportMetrics = () => {
    setSnackbar({
      open: true,
      message: 'Metrics exported successfully',
      severity: 'success',
    });
  };

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading metrics...
        </Typography>
      </Box>
    );
  }

  if (!metrics) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h6" color="error">
          Failed to load metrics data
        </Typography>
      </Box>
    );
  }

  const pieData = [
    { name: 'Success', value: metrics.successRate, color: '#4caf50' },
    { name: 'Failure', value: metrics.failureRate, color: '#f44336' },
  ];

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            Metrics & Analytics
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Comprehensive insights into your CI/CD performance
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              label="Time Range"
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <MenuItem value="24h">Last 24 Hours</MenuItem>
              <MenuItem value="7d">Last 7 Days</MenuItem>
              <MenuItem value="30d">Last 30 Days</MenuItem>
              <MenuItem value="90d">Last 90 Days</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={handleRefresh}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<DownloadIcon />}
            onClick={handleExportMetrics}
          >
            Export
          </Button>
        </Box>
      </Box>

      {/* Key Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SpeedIcon sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography variant="h6">Success Rate</Typography>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {metrics.successRate}%
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Pipeline success rate
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)',
            color: 'white',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <BuildIcon sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography variant="h6">Total Builds</Typography>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {metrics.totalBuilds}
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Builds executed
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)',
            color: 'white',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUpIcon sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography variant="h6">Avg Build Time</Typography>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {formatDuration(metrics.averageBuildTime)}
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Average build duration
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #2196f3 0%, #1976d2 100%)',
            color: 'white',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SuccessIcon sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography variant="h6">Code Coverage</Typography>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {metrics.codeCoverage}%
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Test coverage percentage
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Trends and Performance */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Build Trends Chart */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Build Trends & Performance
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <ComposedChart data={metrics.trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <RechartsTooltip />
                  <Area yAxisId="left" type="monotone" dataKey="success" stackId="1" stroke="#4caf50" fill="#4caf50" fillOpacity={0.6} />
                  <Area yAxisId="left" type="monotone" dataKey="failure" stackId="1" stroke="#f44336" fill="#f44336" fillOpacity={0.6} />
                  <Line yAxisId="right" type="monotone" dataKey="buildTime" stroke="#ff9800" strokeWidth={2} />
                  <Line yAxisId="right" type="monotone" dataKey="pipelineTime" stroke="#2196f3" strokeWidth={2} />
                </ComposedChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Success Rate Distribution */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Success Rate Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ textAlign: 'center', mt: 2 }}>
                <Typography variant="h4" color="success.main" sx={{ fontWeight: 'bold' }}>
                  {metrics.successRate}%
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Overall Success Rate
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Performance Metrics and Top Pipelines */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Performance Metrics */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Performance Metrics
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Metric</TableCell>
                      <TableCell>Current</TableCell>
                      <TableCell>Previous</TableCell>
                      <TableCell>Change</TableCell>
                      <TableCell>Trend</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {metrics.timeMetrics.map((metric) => (
                      <TableRow key={metric.metric}>
                        <TableCell>
                          <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                            {metric.metric}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {metric.metric.includes('Time') ? formatDuration(metric.current) : `${metric.current}%`}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" color="textSecondary">
                            {metric.metric.includes('Time') ? formatDuration(metric.previous) : `${metric.previous}%`}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography 
                            variant="body2" 
                            color={metric.change >= 0 ? 'success.main' : 'error.main'}
                          >
                            {metric.change >= 0 ? '+' : ''}{metric.change.toFixed(1)}%
                          </Typography>
                        </TableCell>
                        <TableCell>
                          {getTrendIcon(metric.trend)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Pipelines */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Top Performing Pipelines
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Pipeline</TableCell>
                      <TableCell>Success Rate</TableCell>
                      <TableCell>Runs</TableCell>
                      <TableCell>Avg Time</TableCell>
                      <TableCell>Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {metrics.topPipelines.map((pipeline) => (
                      <TableRow key={pipeline.name}>
                        <TableCell>
                          <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                            {pipeline.name}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" color="success.main">
                            {pipeline.successRate}%
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {pipeline.totalRuns}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {formatDuration(pipeline.averageTime)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            icon={getStatusIcon(pipeline.status)}
                            label={pipeline.status}
                            color={getStatusColor(pipeline.status) as any}
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Build Distribution by Stage */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Build Distribution by Stage
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={metrics.buildDistribution}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="stage" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <RechartsTooltip />
                  <Bar yAxisId="left" dataKey="count" fill="#2196f3" name="Build Count" />
                  <Bar yAxisId="right" dataKey="successRate" fill="#4caf50" name="Success Rate %" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

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

export default Metrics;
