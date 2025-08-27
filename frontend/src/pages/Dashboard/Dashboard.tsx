import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
  Paper,
  Avatar,
  IconButton,
  Button,
  Tooltip,
  Fab,
} from '@mui/material';
import {
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Schedule as PendingIcon,
  PlayArrow as RunningIcon,
  Timeline as TimelineIcon,
  Add as AddIcon,
  Refresh as RefreshIcon,
  Code as CodeIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon,
  Build as BuildIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';

interface DashboardMetrics {
  totalPipelines: number;
  successRate: number;
  failureRate: number;
  averageBuildTime: number;
  runningPipelines: number;
  pendingPipelines: number;
  totalBuilds: number;
  alertCount: number;
  configChanges: number;
}

interface PipelineStatus {
  id: string;
  name: string;
  status: 'success' | 'failure' | 'running' | 'pending';
  repository: string;
  branch: string;
  startedAt: string;
  duration?: number;
  lastCommit?: string;
  triggerType: 'push' | 'pr' | 'manual' | 'schedule';
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    totalPipelines: 0,
    successRate: 0,
    failureRate: 0,
    averageBuildTime: 0,
    runningPipelines: 0,
    pendingPipelines: 0,
    totalBuilds: 0,
    alertCount: 5,
    configChanges: 12,
  });

  const [recentPipelines, setRecentPipelines] = useState<PipelineStatus[]>([]);
  const [loading, setLoading] = useState(true);

  // Mock data for demonstration
  useEffect(() => {
    setTimeout(() => {
      setMetrics({
        totalPipelines: 156,
        successRate: 87.2,
        failureRate: 12.8,
        averageBuildTime: 8.5,
        runningPipelines: 3,
        pendingPipelines: 2,
        totalBuilds: 1247,
        alertCount: 5,
        configChanges: 12,
      });

      setRecentPipelines([
        {
          id: '1',
          name: 'main-pipeline',
          status: 'success',
          repository: 'myapp/frontend',
          branch: 'main',
          startedAt: '2024-01-15T10:30:00Z',
          duration: 5.2,
          lastCommit: 'a1b2c3d',
          triggerType: 'push',
        },
        {
          id: '2',
          name: 'feature-pipeline',
          status: 'running',
          repository: 'myapp/backend',
          branch: 'feature/auth',
          startedAt: '2024-01-15T10:25:00Z',
          lastCommit: 'e4f5g6h',
          triggerType: 'pr',
        },
        {
          id: '3',
          name: 'deploy-pipeline',
          status: 'failure',
          repository: 'myapp/infrastructure',
          branch: 'main',
          startedAt: '2024-01-15T10:20:00Z',
          duration: 12.1,
          lastCommit: 'i7j8k9l',
          triggerType: 'manual',
        },
        {
          id: '4',
          name: 'test-pipeline',
          status: 'pending',
          repository: 'myapp/testing',
          branch: 'develop',
          startedAt: '2024-01-15T10:15:00Z',
          lastCommit: 'm0n1o2p',
          triggerType: 'schedule',
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

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Loading dashboard data...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header with Actions */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            CI/CD Dashboard
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Monitor your pipelines, builds, and system health in real-time
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Tooltip title="Refresh Data">
            <IconButton color="primary" size="large">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Add Pipeline">
            <Fab color="primary" size="medium">
              <AddIcon />
            </Fab>
          </Tooltip>
        </Box>
      </Box>

      {/* Enhanced Metrics Cards */}
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
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mr: 2 }}>
                  <CodeIcon />
                </Avatar>
                <Typography variant="h6">Total Pipelines</Typography>
              </Box>
              <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                {metrics.totalPipelines}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Active pipelines in system
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
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mr: 2 }}>
                  <TrendingUpIcon />
                </Avatar>
                <Typography variant="h6">Success Rate</Typography>
              </Box>
              <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                {metrics.successRate}%
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Pipeline success percentage
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
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mr: 2 }}>
                  <SpeedIcon />
                </Avatar>
                <Typography variant="h6">Avg Build Time</Typography>
              </Box>
              <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                {formatDuration(metrics.averageBuildTime)}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Average pipeline duration
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
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mr: 2 }}>
                  <BuildIcon />
                </Avatar>
                <Typography variant="h6">Active Builds</Typography>
              </Box>
              <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                {metrics.runningPipelines + metrics.pendingPipelines}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Currently running/pending
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts and Recent Activity */}
      <Grid container spacing={3}>
        {/* Build Trends Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Build Trends (Last 7 Days)
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={[
                    { date: 'Jan 9', success: 12, failure: 2 },
                    { date: 'Jan 10', success: 15, failure: 1 },
                    { date: 'Jan 11', success: 18, failure: 3 },
                    { date: 'Jan 12', success: 14, failure: 2 },
                    { date: 'Jan 13', success: 16, failure: 1 },
                    { date: 'Jan 14', success: 20, failure: 2 },
                    { date: 'Jan 15', success: 17, failure: 1 },
                  ]}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <RechartsTooltip />
                  <Line type="monotone" dataKey="success" stroke="#4caf50" strokeWidth={2} />
                  <Line type="monotone" dataKey="failure" stroke="#f44336" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Pipelines */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                  Recent Pipelines
                </Typography>
                <Button size="small" color="primary">
                  View All
                </Button>
              </Box>
              <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                {recentPipelines.map((pipeline) => (
                  <Paper
                    key={pipeline.id}
                    sx={{
                      p: 2,
                      mb: 2,
                      borderLeft: `4px solid ${
                        pipeline.status === 'success'
                          ? '#4caf50'
                          : pipeline.status === 'failure'
                          ? '#f44336'
                          : pipeline.status === 'running'
                          ? '#2196f3'
                          : '#ff9800'
                      }`,
                    }}
                  >
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="subtitle2" noWrap>
                        {pipeline.name}
                      </Typography>
                      <Chip
                        icon={getStatusIcon(pipeline.status)}
                        label={pipeline.status}
                        color={getStatusColor(pipeline.status) as any}
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="textSecondary" noWrap>
                      {pipeline.repository} • {pipeline.branch}
                    </Typography>
                    {pipeline.duration && (
                      <Typography variant="body2" color="textSecondary">
                        Duration: {formatDuration(pipeline.duration)}
                      </Typography>
                    )}
                  </Paper>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
