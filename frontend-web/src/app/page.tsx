'use client';

import React, { useState, useEffect } from 'react';
import { 
  Home, 
  ShoppingCart, 
  CheckSquare, 
  Wallet, 
  Lightbulb, 
  Cpu, 
  Globe, 
  Calendar as CalendarIcon,
  Activity,
  User,
  Settings,
  Bell,
  RefreshCw
} from 'lucide-react';
import { choresApi, inventoryApi, financeApi, agentApi } from '@/lib/api';

const DashboardCard = ({ title, value, icon: Icon, color, description }: any) => (
  <div className="glass rounded-2xl p-6 card-hover">
    <div className="flex justify-between items-start mb-4">
      <div className={`p-3 rounded-xl bg-${color}/10 text-${color}`}>
        <Icon size={24} />
      </div>
      <span className="text-xs text-muted-foreground font-medium">{description}</span>
    </div>
    <h3 className="text-sm font-medium text-muted-foreground mb-1">{title}</h3>
    <p className="text-2xl font-bold text-white">{value}</p>
  </div>
);

const SidebarItem = ({ icon: Icon, label, active = false }: any) => (
  <div className={`flex items-center gap-3 px-4 py-3 rounded-xl cursor-default transition-all ${active ? 'bg-primary/20 text-primary border border-primary/20' : 'text-muted-foreground hover:bg-white/5 hover:text-white'}`}>
    <Icon size={20} />
    <span className="font-medium text-sm">{label}</span>
  </div>
);

export default function HomeDashboard() {
  const [stats, setStats] = useState({
    pendingChores: 0,
    overdueChores: 0,
    inventoryCount: 0,
    lowStockStock: 0,
    budgetBalance: 0,
    activeAgents: 9
  });
  const [activities, setActivities] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [chores, inventory, lowStock, finance] = await Promise.all([
        choresApi.list(),
        inventoryApi.list(),
        inventoryApi.getLowStock(),
        financeApi.getSummary()
      ]);

      setStats({
        pendingChores: chores.filter((c: any) => !c.completed_at).length,
        overdueChores: chores.filter((c: any) => !c.completed_at && c.due_date && new Date(c.due_date) < new Date()).length,
        inventoryCount: inventory.length,
        lowStockStock: lowStock.length,
        budgetBalance: finance.net_balance,
        activeAgents: 9
      });

      // Mock activities if empty
      setActivities([
        { agent: 'ChoreCoordinatorAgent', message: 'Ready to assign new tasks.', time: 'Just now', icon: CheckSquare, color: 'primary' },
        { agent: 'InventoryAgent', message: `Found ${lowStock.length} items low in stock.`, time: '5 mins ago', icon: ShoppingCart, color: 'accent' },
        { agent: 'FinanceAgent', message: `Budget balance is $${finance.net_balance.toFixed(2)}.`, time: '10 mins ago', icon: Wallet, color: 'indigo' }
      ]);

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Auto refresh every 30s
    return () => clearInterval(interval);
  }, []);

const [isChatOpen, setIsChatOpen] = useState(false);
  const [prompt, setPrompt] = useState('');
  const [chatHistory, setChatHistory] = useState<any[]>([]);

  const handleAgentRequest = async () => {
    if (!prompt.trim()) return;
    const userMsg = { role: 'user', content: prompt };
    setChatHistory([...chatHistory, userMsg]);
    const currentPrompt = prompt;
    setPrompt('');
    
    try {
      const response = await agentApi.submitRequest(currentPrompt);
      const assistantMsg = response.result.messages[0];
      setChatHistory(prev => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Agent error:', error);
      setChatHistory(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error processing your request.' }]);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 p-6 flex flex-col gap-8">
        <div className="flex items-center gap-3 px-2">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
            <span className="text-white font-bold text-xl">P</span>
          </div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">PICK-E</h1>
        </div>

        <nav className="flex flex-col gap-2">
          <SidebarItem icon={Home} label="Dashboard" active />
          <SidebarItem icon={CheckSquare} label="Chores" />
          <SidebarItem icon={ShoppingCart} label="Inventory" />
          <SidebarItem icon={Wallet} label="Finance" />
          <SidebarItem icon={CalendarIcon} label="Calendar" />
          <SidebarItem icon={Lightbulb} label="Ideas" />
          <SidebarItem icon={Globe} label="Geopolitics" />
          <SidebarItem icon={Cpu} label="Tech Intelligence" />
        </nav>

        <div className="mt-auto flex flex-col gap-2 pt-6 border-t border-white/5">
          <SidebarItem icon={Settings} label="Settings" />
          <SidebarItem icon={User} label="Profile" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">Welcome Home, Assistant</h2>
            <p className="text-muted-foreground">Today is Dec 25, 2025. Here's what's happening.</p>
          </div>
          <div className="flex gap-4">
            <button 
              onClick={fetchData} 
              className={`glass p-3 rounded-xl text-muted-foreground hover:text-white transition-all ${isLoading ? 'animate-spin' : ''}`}
            >
              <RefreshCw size={20} />
            </button>
            <button className="glass p-3 rounded-xl text-muted-foreground hover:text-white transition-colors">
              <Bell size={20} />
            </button>
            <div className="glass px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500"></div>
              <span className="text-sm font-medium text-white">YCS Household</span>
            </div>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <DashboardCard title="Pending Chores" value={isLoading ? '...' : stats.pendingChores} icon={CheckSquare} color="primary" description={`${stats.overdueChores} overdue`} />
          <DashboardCard title="Shopping List" value={isLoading ? '...' : `${stats.inventoryCount} Items`} icon={ShoppingCart} color="accent" description={`${stats.lowStockStock} low stock`} />
          <DashboardCard title="Monthly Balance" value={isLoading ? '...' : `$${stats.budgetBalance.toFixed(2)}`} icon={Wallet} color="primary" description="Updated just now" />
          <DashboardCard title="Active Agents" value={stats.activeAgents} icon={Activity} color="accent" description="All systems normal" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Activity Area */}
          <div className="lg:col-span-2 flex flex-col gap-8">
            <section className="glass rounded-3xl p-8">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-white">Recent Agent Activity</h3>
                <button className="text-sm text-primary font-medium hover:underline">View All</button>
              </div>
              <div className="flex flex-col gap-6">
                {activities.map((act, i) => (
                  <div key={i} className="flex gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 group hover:bg-white/10 transition-all">
                    <div className={`w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400`}>
                      <act.icon size={20} />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-white">{act.agent}</h4>
                      <p className="text-sm text-muted-foreground">{act.message}</p>
                      <span className="text-xs text-muted-foreground/60 mt-1 block">{act.time}</span>
                    </div>
                  </div>
                ))}
                {activities.length === 0 && !isLoading && (
                  <div className="text-center py-10">
                    <p className="text-muted-foreground">No recent agent activity.</p>
                  </div>
                )}
              </div>
            </section>

            {/* Chat Area */}
            {isChatOpen && (
              <section className="glass rounded-3xl p-8 flex flex-col gap-4 max-h-[500px]">
                <div className="flex justify-between items-center">
                  <h3 className="text-xl font-bold text-white">Manager Agent Chat</h3>
                  <button onClick={() => setIsChatOpen(false)} className="text-muted-foreground">Close</button>
                </div>
                <div className="flex-1 overflow-y-auto flex flex-col gap-4 p-4">
                  {chatHistory.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] px-4 py-2 rounded-2xl text-sm ${msg.role === 'user' ? 'bg-primary text-white' : 'bg-white/10 text-white'}`}>
                        {msg.content}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleAgentRequest()}
                    placeholder="Ask the manager anything..."
                    className="flex-1 glass bg-white/5 rounded-xl px-4 py-2 text-white outline-none focus:border-primary/50 transition-all"
                  />
                  <button onClick={handleAgentRequest} className="bg-primary px-4 py-2 rounded-xl text-white font-bold">Send</button>
                </div>
              </section>
            )}
          </div>

          {/* Sidebar Area */}
          <div className="flex flex-col gap-8">
            <section className="glass rounded-3xl p-8">
              <h3 className="text-xl font-bold text-white mb-6">Agent Control Center</h3>
              <div className="flex flex-col gap-3">
                <button 
                  onClick={() => setIsChatOpen(true)}
                  className="w-full py-4 rounded-2xl bg-primary text-white font-bold text-sm shadow-lg shadow-primary/20 hover:opacity-90 transition-all"
                >
                  Talk to Manager Agent
                </button>
                <button className="w-full py-4 rounded-2xl bg-white/5 text-white font-bold text-sm border border-white/10 hover:bg-white/10 transition-all cursor-not-allowed opacity-50">
                  Sync External Tools
                </button>
                <button className="w-full py-4 rounded-2xl bg-white/5 text-white font-bold text-sm border border-white/10 hover:bg-white/10 transition-all cursor-not-allowed opacity-50">
                  Generate Today's Briefing
                </button>
              </div>
            </section>

            <section className="glass rounded-3xl p-8">
              <h3 className="text-xl font-bold text-white mb-6">System Health</h3>
              <div className="flex flex-col gap-4">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Database (SQLite)</span>
                  <span className="text-emerald-400 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400"></div> Connected
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Manager Engine</span>
                  <span className="text-emerald-400 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400"></div> Online
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Frontend (Turbopack)</span>
                  <span className="text-emerald-400 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400"></div> Ready
                  </span>
                </div>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
