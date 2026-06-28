"use client"
import React, { useEffect, useState } from 'react'
import { StatCard } from '@/components/dashboard/StatCard'
import { ChartsPanel } from '@/components/dashboard/ChartsPanel'
import { AIChat } from '@/components/dashboard/AIChat'
import { fetchReviews, triggerAnalysis, fetchDashboardStats } from '@/lib/api'
import { MessageSquare, Star, Zap, Upload } from 'lucide-react'
import { Button } from '@/components/ui/button'

const SimpleButton = ({ onClick, children, className, disabled }: any) => (
  <button onClick={onClick} disabled={disabled} className={`px-4 py-2 bg-green-500 text-black font-semibold rounded-full hover:bg-green-400 transition disabled:opacity-75 disabled:cursor-wait ${className}`}>
    {children}
  </button>
)

export default function DashboardPage() {
  const [reviews, setReviews] = useState<any[]>([])
  const [dashboardStats, setDashboardStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  const loadData = async () => {
    setLoading(true)
    try {
      const revs = await fetchReviews()
      setReviews(revs || [])
      const stats = await fetchDashboardStats()
      setDashboardStats(stats)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const [analyzing, setAnalyzing] = useState(false)

  const handleAnalyze = async () => {
    setAnalyzing(true)
    try {
      await triggerAnalysis()
      alert("Analysis completed successfully!")
      loadData() // Refresh dashboard data if any
    } catch (e) {
      alert("Analysis failed!")
      console.error(e)
    } finally {
      setAnalyzing(false)
    }
  }

  // Dynamic or Mock data for charts
  const sentimentData = dashboardStats?.sentiment_data || [
    { name: 'Positive', value: 400 },
    { name: 'Negative', value: 300 },
    { name: 'Neutral', value: 300 },
  ]
  const platformData = dashboardStats?.platform_data || [
    { name: 'Google Play', value: 400 },
    { name: 'Reddit', value: 300 },
    { name: 'Community', value: 200 },
    { name: 'CSV', value: 100 },
  ]
  const priorityData = dashboardStats?.priority_data || [
    { name: 'High', value: 150 },
    { name: 'Medium', value: 300 },
    { name: 'Low', value: 550 },
  ]

  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      <div className="max-w-[1600px] mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Review Discovery Engine</h1>
            <p className="text-gray-400 mt-1">AI-powered insights for Spotify Product Managers.</p>
          </div>
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <SimpleButton onClick={handleAnalyze} disabled={analyzing} className="flex items-center gap-2 min-w-[160px] justify-center">
              {analyzing ? (
                <div className="h-4 w-4 rounded-full border-2 border-black border-t-transparent animate-spin" />
              ) : (
                <Zap className="h-4 w-4" />
              )}
              {analyzing ? "Analyzing..." : "Run AI Analysis"}
            </SimpleButton>
            <SimpleButton className="bg-gray-800 text-white hover:bg-gray-700 flex items-center gap-2">
              <Upload className="h-4 w-4" /> Upload CSV
            </SimpleButton>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard 
            title="Total Reviews" 
            value={dashboardStats?.total_reviews || reviews.length || 1042} 
            icon={MessageSquare} 
            description="Analyzed by AI"
          />
          <StatCard 
            title="Average Rating" 
            value="3.8" 
            icon={Star} 
            description="Across all platforms"
          />
          <StatCard 
            title="Top Pain Point" 
            value={dashboardStats?.top_pain_point || "App Crashing"} 
            icon={Zap} 
            description="Identified by Gemini"
          />
          <StatCard 
            title="Top Request" 
            value={dashboardStats?.top_request || "HiFi Audio"} 
            icon={Star} 
            description="Most requested feature"
          />
        </div>

        {/* Main Content Layout: Charts (Left) & Chat (Right) */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2">
            <ChartsPanel 
              sentimentData={sentimentData} 
              platformData={platformData} 
              priorityData={priorityData} 
            />
          </div>
          <div className="xl:col-span-1">
            <AIChat />
          </div>
        </div>

      </div>
    </div>
  )
}
