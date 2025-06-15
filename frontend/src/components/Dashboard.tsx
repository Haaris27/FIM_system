'use client'
import { Title } from "@tremor/react"
import { useEffect, useState } from "react"
import { MetricCard } from "./MetricCard"
import { FileList } from "./FileList"
import { MonitoredFile, MonitoringData } from '@/utils/types'

export default function Dashboard() {
  const [monitoringData, setMonitoringData] = useState<MonitoringData>({
    monitored: [],
    total: 0
  })
  const [changeHistory, setChangeHistory] = useState<MonitoredFile[]>([])
  const [deletedFiles, setDeletedFiles] = useState<Set<string>>(new Set())
  const [previousFiles, setPreviousFiles] = useState<Set<string>>(new Set())

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/files', {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setMonitoringData(data);
        
        const currentFilePaths = new Set<string>(
          data.monitored.map((f: MonitoredFile) => f.path)
        )
        
        previousFiles.forEach(path => {
          if (!currentFilePaths.has(path)) {
            const newDeletedFile: MonitoredFile = {
              path,
              status: 'DELETED',
              lastModified: new Date().toISOString(),
              hash: ''
            }
            setDeletedFiles(prev => new Set([...Array.from(prev), path]))
            setChangeHistory(prev => [...prev, newDeletedFile])
          }
        })
        
        setPreviousFiles(currentFilePaths)
        
        const changedFiles = data.monitored.filter((f: MonitoredFile) => f.status !== "UNCHANGED")
        if (changedFiles.length > 0) {
          setChangeHistory(prev => [...prev, ...changedFiles])
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setMonitoringData({ monitored: [], total: 0 });
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [previousFiles])

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-950 via-purple-900 to-indigo-950 p-4 md:p-10 relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('/infinity.svg')] opacity-5 animate-pulse"></div>
      <div className="absolute inset-0 bg-gradient-radial from-violet-600/20 via-transparent to-transparent"></div>
      <div className="mx-auto max-w-7xl relative z-10">
        <Title className="text-5xl font-bold text-white mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-violet-300 to-purple-200">
          File Integrity Monitoring System
        </Title>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-8">
          <div className="transform hover:scale-105 transition-transform duration-200">
            <MetricCard 
              title="Files Monitored" 
              value={monitoringData.total}
              icon="shield"
            />
          </div>
          <div className="transform hover:scale-105 transition-transform duration-200">
            <MetricCard 
              title="Changes Detected" 
              value={changeHistory.length}
              icon="alert"
            />
          </div>
          <div className="transform hover:scale-105 transition-transform duration-200">
            <MetricCard 
              title="Files Deleted" 
              value={deletedFiles.size}
              icon="warning"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-3">
            <div className="transform hover:scale-100 transition-transform duration-200">
              <FileList 
                files={monitoringData.monitored} 
                changeHistory={changeHistory}
                deletedFiles={Array.from(deletedFiles)}
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}