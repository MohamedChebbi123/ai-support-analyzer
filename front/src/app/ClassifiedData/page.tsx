'use client'
import React, { useEffect, useState } from 'react'
import { FiAlertTriangle, FiInfo, FiCheckCircle, FiClock, FiUser, FiMail, FiPhone, FiGlobe, FiCalendar, FiType } from 'react-icons/fi'

interface DataItem {
  name: string
  lastname: string
  country: string
  email: string
  phone_number: string
  problem: string
  submission_date: string
  problem_priority: 'low' | 'medium' | 'high' | 'critical'
  problem_type: string
}

const priorityColors = {
  low: 'bg-blue-100 text-blue-800',
  medium: 'bg-green-100 text-green-800',
  high: 'bg-yellow-100 text-yellow-800',
  critical: 'bg-red-100 text-red-800'
}

const priorityIcons = {
  low: <FiInfo className="mr-1" />,
  medium: <FiCheckCircle className="mr-1" />,
  high: <FiAlertTriangle className="mr-1" />,
  critical: <FiAlertTriangle className="mr-1" />
}

const Datapage: React.FC = () => {
  const [data, setData] = useState<DataItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/fetchclassifeiddata")
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const responseData = await response.json()
        setData(responseData)
      } catch (err) {
        console.error("Fetch error:", err)
        setError(err instanceof Error ? err.message : 'An unknown error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-md">
          <h2 className="font-bold text-lg">Error loading data</h2>
          <p>{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-2 bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!data.length) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded max-w-md">
          <h2 className="font-bold text-lg">No data available</h2>
          <p>There are currently no submissions to display.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Customer Support Submissions</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {data.map((item, idx) => (
          <div key={idx} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
            <div className="p-6">
              <div className="flex items-center mb-4">
                <div className="bg-indigo-100 p-3 rounded-full mr-4">
                  <FiUser className="text-indigo-600 text-xl" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">{item.name} {item.lastname}</h2>
                  <p className="text-gray-500">{item.country}</p>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center text-gray-600">
                  <FiMail className="mr-2 text-gray-400" />
                  <a href={`mailto:${item.email}`} className="hover:text-indigo-600 hover:underline">
                    {item.email}
                  </a>
                </div>

                <div className="flex items-center text-gray-600">
                  <FiPhone className="mr-2 text-gray-400" />
                  <a href={`tel:${item.phone_number}`} className="hover:text-indigo-600">
                    {item.phone_number}
                  </a>
                </div>

                <div className="flex items-center text-gray-600">
                  <FiCalendar className="mr-2 text-gray-400" />
                  <span>{formatDate(item.submission_date)}</span>
                </div>

                <div className="flex items-center text-gray-600">
                  <FiType className="mr-2 text-gray-400" />
                  <span>{item.problem_type}</span>
                </div>

                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium 
                  ${priorityColors[item.problem_priority]}`}>
                  {priorityIcons[item.problem_priority]}
                  {item.problem_priority.charAt(0).toUpperCase() + item.problem_priority.slice(1)}
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-100">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Problem Description</h3>
                <p className="text-gray-700">{item.problem}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Datapage