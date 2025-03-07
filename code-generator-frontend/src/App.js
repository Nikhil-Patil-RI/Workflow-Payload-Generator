import React, { useState, useEffect } from 'react';
import './App.css';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import axios from 'axios';

const API_URL = 'http://localhost:8001';

const sampleWorkflow = {
  nodes: [
    {
      node_id: "node1",
      tools_to_use: [
        {
          tool_id: 1,
          tool_name: "EmailSender",
          tool_params: {
            items: [
              { field_name: "user_email", user_dependent: true },
              { field_name: "user_name", user_dependent: true },
              { field_name: "template_id", user_dependent: false }
            ]
          }
        }
      ]
    },
    {
      node_id: "node2",
      tools_to_use: [
        {
          tool_id: 2,
          tool_name: "LeaveRequest",
          tool_params: {
            items: [
              { field_name: "employee_name", user_dependent: true },
              { field_name: "requested_days", user_dependent: true },
              { field_name: "current_reason", user_dependent: false }
            ]
          }
        }
      ]
    }
  ],
  connections: [
    {
      from_node: "node1",
      to: "node2",
      conditional_routing: "success"
    }
  ]
};

const languageOptions = [
  { id: 'curl', name: 'cURL', syntaxHighlight: 'bash' },
  { id: 'python', name: 'Python API', syntaxHighlight: 'python' },
  { id: 'js', name: 'JS API', syntaxHighlight: 'javascript' },
  { id: 'ts', name: 'TS API', syntaxHighlight: 'typescript' }
];

function App() {
  const [activeTab, setActiveTab] = useState('curl');
  const [loading, setLoading] = useState(false);
  const [code, setCode] = useState('');
  const [payload, setPayload] = useState({});
  const [error, setError] = useState(null);
  const [baseUrl, setBaseUrl] = useState("https://forty-needles-draw.loca.lt");

  const fetchCode = async (language) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_URL}/generate-code`, {
        workflow: sampleWorkflow,
        language: language,
        base_url: baseUrl
      });
      
      setCode(response.data.code);
      setPayload(response.data.payload);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while fetching code');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCode(activeTab);
  }, [activeTab]);

  const  getSyntaxHighlightLanguage = () => {
    const option = languageOptions.find(opt => opt.id === activeTab);
    return option ? option.syntaxHighlight : 'text';
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    alert('Code copied to clipboard!');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Workflow Code Generator</h1>
        <p>Generate code to test your workflow execution server.</p>
      </header>

      <main className="App-main">
        <div className="api-config">
          <div className="config-field">
            <label>Base URL:</label>
            <input 
              type="text" 
              value={baseUrl} 
              onChange={(e) => setBaseUrl(e.target.value)} 
            />
          </div>
          <button onClick={() => fetchCode(activeTab)}>Update Configuration</button>
        </div>

        <div className="tabs">
          {languageOptions.map(option => (
            <button
              key={option.id}
              className={activeTab === option.id ? 'active' : ''}
              onClick={() => setActiveTab(option.id)}
            >
              {option.name}
            </button>
          ))}
        </div>

        <div className="code-container">
          <div className="code-header">
            <button className="copy-button" onClick={copyToClipboard}>
              Copy Code
            </button>
          </div>
          
          {loading ? (
            <div className="loading">Loading...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : (
            <SyntaxHighlighter
              language={getSyntaxHighlightLanguage()}
              style={vscDarkPlus}
              wrapLines={true}
            >
              {code}
            </SyntaxHighlighter>
          )}
        </div>

        <div className="payload-container">
          <h3>Generated Payload</h3>
          <SyntaxHighlighter language="json" style={vscDarkPlus}>
            {JSON.stringify(payload, null, 2)}
          </SyntaxHighlighter>
        </div>
      </main>
    </div>
  );
}

export default App;