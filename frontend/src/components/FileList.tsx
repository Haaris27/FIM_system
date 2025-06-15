import { Card, Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Title } from "@tremor/react";
import { StatusBadge } from "./StatusBadge";
import { format } from "date-fns";
import { MonitoredFile } from "@/utils/types";

interface FileListProps {
  files: MonitoredFile[];
  changeHistory: MonitoredFile[];
  deletedFiles?: string[];
}

export function FileList({ files, changeHistory, deletedFiles }: FileListProps) {
  return (
    <div className="space-y-6">
      <Card className="bg-purple-900/40 backdrop-blur-xl border border-violet-400/20 relative overflow-hidden group animate-glow">
        <div className="absolute inset-0 bg-gradient-to-r from-violet-600/20 via-purple-500/20 to-violet-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <Table className="text-white">
          <TableHead>
            <TableRow>
              <TableHeaderCell>File Path</TableHeaderCell>
              <TableHeaderCell>Status</TableHeaderCell>
              <TableHeaderCell>Last Modified</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {files.map((file, index) => (
              <TableRow key={index}>
                <TableCell>{file.path}</TableCell>
                <TableCell><StatusBadge status={file.status} /></TableCell>
                <TableCell>{format(new Date(file.lastModified), 'PPpp')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
      
      <Card className="bg-white/10 backdrop-blur-lg border border-white/20">
        <Title className="text-white mb-4">Change History</Title>
        <Table className="text-white">
          <TableHead>
            <TableRow>
              <TableHeaderCell>File Path</TableHeaderCell>
              <TableHeaderCell>Status</TableHeaderCell>
              <TableHeaderCell>Time</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {changeHistory.map((file, index) => (
              <TableRow key={index}>
                <TableCell>{file.path}</TableCell>
                <TableCell>
                  <StatusBadge status={file.status} />
                </TableCell>
                <TableCell>{format(new Date(file.lastModified), 'PPpp')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}