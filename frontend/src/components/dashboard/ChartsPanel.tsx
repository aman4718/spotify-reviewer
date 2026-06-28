"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts'

interface ChartsPanelProps {
  sentimentData: { name: string; value: number }[];
  platformData: { name: string; value: number }[];
  priorityData: { name: string; value: number }[];
}

const COLORS = ['#1DB954', '#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6'];

export function ChartsPanel({ sentimentData, platformData, priorityData }: ChartsPanelProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      
      {/* Sentiment Distribution */}
      <Card className="bg-black/40 border-green-900/50 backdrop-blur-xl">
        <CardHeader>
          <CardTitle className="text-sm font-medium text-gray-300">Sentiment Distribution</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#000', borderColor: '#1DB954', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
              <Legend wrapperStyle={{ color: '#aaa' }} />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Platform Distribution */}
      <Card className="bg-black/40 border-green-900/50 backdrop-blur-xl">
        <CardHeader>
          <CardTitle className="text-sm font-medium text-gray-300">Platform Sources</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={platformData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#888" fontSize={12} />
              <YAxis stroke="#888" fontSize={12} />
              <Tooltip 
                cursor={{ fill: '#222' }}
                contentStyle={{ backgroundColor: '#000', borderColor: '#1DB954', color: '#fff' }}
              />
              <Bar dataKey="value" fill="#1DB954" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Issue Priority */}
      <Card className="bg-black/40 border-green-900/50 backdrop-blur-xl">
        <CardHeader>
          <CardTitle className="text-sm font-medium text-gray-300">Issue Priority</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={priorityData} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis type="number" stroke="#888" fontSize={12} />
              <YAxis dataKey="name" type="category" stroke="#888" fontSize={12} />
              <Tooltip 
                cursor={{ fill: '#222' }}
                contentStyle={{ backgroundColor: '#000', borderColor: '#1DB954', color: '#fff' }}
              />
              <Bar dataKey="value" fill="#f59e0b" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

    </div>
  )
}
