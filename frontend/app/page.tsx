import React from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  BookOpen, 
  Search, 
  Users, 
  Target, 
  MessageSquare, 
  TrendingUp, 
  Shield, 
  Zap,
  ArrowRight,
  CheckCircle
} from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-research-50 via-white to-academic-50 dark:from-research-950 dark:via-gray-900 dark:to-academic-950 py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-center mb-6">
              <BookOpen className="h-16 w-16 text-research-600" />
            </div>
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Find Your Perfect
              <span className="text-research-600 block">Research Match</span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
              Connect students with professors whose research areas align with their interests, 
              and help professors discover students that match their active projects.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section - Moved Up */}
      <section className="py-20 bg-research-600">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Find Your Research Match?
          </h2>
          <p className="text-xl text-research-100 mb-8 max-w-2xl mx-auto">
            Join thousands of students and professors who have already found their perfect research partnerships.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/onboarding">
              <Button size="lg" variant="secondary" className="px-8 py-3">
                Get Started Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/search">
              <Button size="lg" variant="outline" className="px-8 py-3 border-white text-white hover:bg-white hover:text-research-600">
                Browse Opportunities
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-research-600 mb-2">500+</div>
              <div className="text-gray-600 dark:text-gray-400">Active Students</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-research-600 mb-2">200+</div>
              <div className="text-gray-600 dark:text-gray-400">Professors</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-research-600 mb-2">150+</div>
              <div className="text-gray-600 dark:text-gray-400">Research Projects</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-research-600 mb-2">95%</div>
              <div className="text-gray-600 dark:text-gray-400">Match Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose MatchEd?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Our intelligent matching system and comprehensive platform make finding research opportunities easier than ever.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 bg-research-100 dark:bg-research-900 rounded-lg flex items-center justify-center mb-4">
                  <Target className="h-6 w-6 text-research-600" />
                </div>
                <CardTitle>Smart Matching</CardTitle>
                <CardDescription>
                  AI-powered algorithm that considers interests, skills, availability, and research alignment
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 bg-research-100 dark:bg-research-900 rounded-lg flex items-center justify-center mb-4">
                  <Zap className="h-6 w-6 text-research-600" />
                </div>
                <CardTitle>Quick Setup</CardTitle>
                <CardDescription>
                  Complete your profile in minutes with our guided onboarding process
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 bg-research-100 dark:bg-research-900 rounded-lg flex items-center justify-center mb-4">
                  <MessageSquare className="h-6 w-6 text-research-600" />
                </div>
                <CardTitle>Direct Communication</CardTitle>
                <CardDescription>
                  Built-in messaging system to connect with potential matches instantly
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 bg-research-100 dark:bg-research-900 rounded-lg flex items-center justify-center mb-4">
                  <Shield className="h-6 w-6 text-research-600" />
                </div>
                <CardTitle>Privacy First</CardTitle>
                <CardDescription>
                  Control your profile visibility and protect your personal information
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 bg-research-100 dark:bg-research-900 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="h-6 w-6 text-research-600" />
                </div>
                <CardTitle>Track Progress</CardTitle>
                <CardDescription>
                  Monitor your application status and research progress in real-time
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 bg-research-100 dark:bg-research-900 rounded-lg flex items-center justify-center mb-4">
                  <Users className="h-6 w-6 text-research-600" />
                </div>
                <CardTitle>Community</CardTitle>
                <CardDescription>
                  Join a network of researchers and students from top institutions worldwide
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Get started in three simple steps and find your perfect research opportunity
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-research-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                1
              </div>
              <h3 className="text-xl font-semibold mb-4">Create Your Profile</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Sign up and complete your profile with research interests, skills, and availability
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-research-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                2
              </div>
              <h3 className="text-xl font-semibold mb-4">Discover Matches</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Our algorithm finds professors and projects that align with your profile
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-research-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                3
              </div>
              <h3 className="text-xl font-semibold mb-4">Connect & Apply</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Message potential matches and apply to research opportunities
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
