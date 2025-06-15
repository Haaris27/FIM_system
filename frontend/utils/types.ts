export interface MonitoredFile {
  path: string;
  lastModified: string;
  status: 'NEW' | 'CHANGED' | 'UNCHANGED' | 'DELETED';
  hash: string;
}

export interface MonitoringData {
  monitored: MonitoredFile[];
  total: number;
}
