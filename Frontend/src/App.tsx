import React, { useState, useEffect, useRef } from 'react';
import { Search } from 'lucide-react';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showContact, setShowContact] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState('');
  const [personality, setPersonality] = useState('naval');
  const [cycling, setCycling] = useState(true);
  const [currentHeading, setCurrentHeading] = useState('naval');
  const [searchCount, setSearchCount] = useState(0);
  const [showEmailPopup, setShowEmailPopup] = useState(true);
  const [email, setEmail] = useState('');
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  const [isClosingEmailBox, setIsClosingEmailBox] = useState(false);
  const personalities = [
    { key: 'naval', label: 'Ask Naval' },
    { key: 'peter', label: 'Ask Peter' },
    { key: 'paul', label: 'Ask Paul' },
    { key: 'sama', label: 'Ask Sama' },
    { key: 'charlie', label: 'Ask Charlie' }
  ];
  const cycleIndex = useRef(0);
  const typingTimeout = useRef<number | null>(null);
  const cyclingTimeout = useRef<number | null>(null);

  // Profile data for side panel
  const profiles = [
    {
      key: 'naval',
      img: '/personalitiesimgs/naval ravikantimg.jpg',
      first: 'naval',
      last: 'ravikant',
    },
    {
      key: 'peter',
      img: '/personalitiesimgs/peterthielimg.jpg',
      first: 'peter',
      last: 'thiel',
    },
    {
      key: 'paul',
      img: '/personalitiesimgs/paulgrahamimg.png',
      first: 'paul',
      last: 'graham',
    },
    {
      key: 'sama',
      img: '/personalitiesimgs/samaltmanimg.jpg',
      first: 'sam',
      last: 'altman',
    },
    {
      key: 'charlie',
      img: '/personalitiesimgs/charliemungerimg.jpg',
      first: 'charlie',
      last: 'munger',
    },
  ];
  const [hoveredProfile, setHoveredProfile] = useState<string | null>(null);

  useEffect(() => {
    if (!cycling) return;
    const interval = setInterval(() => {
      cycleIndex.current = (cycleIndex.current + 1) % personalities.length;
      setCurrentHeading(personalities[cycleIndex.current].key);
    }, 1500);
    return () => clearInterval(interval);
  }, [cycling, personalities.length]);

  useEffect(() => {
    if (!cycling) {
      setCurrentHeading(personality);
    }
  }, [cycling, personality]);

  const handlePersonalityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setPersonality(e.target.value);
    setCycling(false);
  };

  const handleBackgroundClick = () => {
    if (showContact) {
      setShowContact(false);
    }
    // Removed automatic theme toggle - users can manually toggle if needed
  };

  const handleSearchClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  const handleContactClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowContact(!showContact);
  };

  // Backend URL - Replace with your actual Render backend URL
  const BACKEND_URL = 'https://randomdomain-akbkd8dgewebdudm.southeastasia-01.azurewebsites.net/';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setResponse('');

    try {
      const response = await fetch(`${BACKEND_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: searchQuery, personality }),
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data.answer);
        setSearchCount(count => count + 1);
      } else {
        console.error('Backend error:', response.status, response.statusText);
        setResponse('Sorry, I encountered an error. Please try again.');
      }
    } catch (error) {
      console.error('Network error:', error);
      setResponse('Sorry, I cannot connect to the server. Please make sure the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setEmailSubmitted(true);
    setShowEmailPopup(false);
  };

  return (
    <div 
      className={`min-h-screen relative overflow-hidden transition-all duration-700 ease-in-out cursor-pointer ${
        isDarkMode ? 'bg-gray-900' : 'bg-white'
      }`}
      onClick={handleBackgroundClick}
    >
      {/* Contact - Top Right */}
      <div className="absolute top-6 right-6 z-20">
        <button 
          className={`text-sm font-light transition-colors duration-300 hover:opacity-70 ${
            isDarkMode ? 'text-white' : 'text-black'
          }`}
          onClick={handleContactClick}
        >
          contact
        </button>
      </div>

      {/* Contact Email Slide */}
      <div className={`fixed top-6 left-6 z-30 transition-all duration-500 ease-out ${
        showContact 
          ? 'transform translate-x-0 opacity-100' 
          : 'transform -translate-x-full opacity-0'
      }`}>
        <div className={`text-sm font-light ${
          isDarkMode ? 'text-white' : 'text-black'
        }`}>
          mail: bharatgupta091107@gmail.com
        </div>
      </div>

      {/* Weird flowing gradient from bottom */}
      <div className="absolute inset-0 pointer-events-none">
        <div 
          className={`absolute bottom-0 left-0 right-0 h-96 transition-opacity duration-700 ${
            isDarkMode ? 'opacity-50' : 'opacity-30'
          }`}
          style={{
            background: `
              radial-gradient(ellipse 120% 80% at 20% 100%, 
                ${isDarkMode ? 'rgba(255, 107, 132, 0.6)' : 'rgba(255, 107, 132, 0.4)'} 0%, 
                ${isDarkMode ? 'rgba(255, 107, 132, 0.3)' : 'rgba(255, 107, 132, 0.2)'} 25%,
                transparent 50%
              ),
              radial-gradient(ellipse 100% 70% at 70% 100%, 
                ${isDarkMode ? 'rgba(126, 87, 194, 0.7)' : 'rgba(126, 87, 194, 0.5)'} 0%, 
                ${isDarkMode ? 'rgba(126, 87, 194, 0.4)' : 'rgba(126, 87, 194, 0.3)'} 30%,
                transparent 60%
              ),
              radial-gradient(ellipse 150% 90% at 50% 100%, 
                ${isDarkMode ? 'rgba(6, 182, 212, 0.5)' : 'rgba(6, 182, 212, 0.3)'} 0%, 
                ${isDarkMode ? 'rgba(6, 182, 212, 0.2)' : 'rgba(6, 182, 212, 0.1)'} 40%,
                transparent 70%
              ),
              radial-gradient(ellipse 80% 60% at 90% 100%, 
                ${isDarkMode ? 'rgba(245, 158, 11, 0.6)' : 'rgba(245, 158, 11, 0.4)'} 0%, 
                ${isDarkMode ? 'rgba(245, 158, 11, 0.3)' : 'rgba(245, 158, 11, 0.2)'} 35%,
                transparent 65%
              ),
              linear-gradient(180deg, 
                transparent 0%, 
                ${isDarkMode ? 'rgba(139, 92, 246, 0.08)' : 'rgba(139, 92, 246, 0.05)'} 60%,
                ${isDarkMode ? 'rgba(236, 72, 153, 0.12)' : 'rgba(236, 72, 153, 0.08)'} 80%,
                ${isDarkMode ? 'rgba(14, 165, 233, 0.09)' : 'rgba(14, 165, 233, 0.06)'} 100%
              )
            `
          }}
        />
        
        {/* Additional flowing elements */}
        <div 
          className={`absolute bottom-0 left-1/4 w-32 h-32 rounded-full animate-pulse transition-all duration-700 ${
            isDarkMode ? 'opacity-30' : 'opacity-20'
          }`}
          style={{
            background: `radial-gradient(circle, ${
              isDarkMode ? 'rgba(167, 139, 250, 0.8)' : 'rgba(167, 139, 250, 0.6)'
            } 0%, transparent 70%)`,
            animation: 'float 8s ease-in-out infinite'
          }}
        />
        <div 
          className={`absolute bottom-10 right-1/3 w-24 h-24 rounded-full animate-pulse transition-all duration-700 ${
            isDarkMode ? 'opacity-25' : 'opacity-15'
          }`}
          style={{
            background: `radial-gradient(circle, ${
              isDarkMode ? 'rgba(236, 72, 153, 0.7)' : 'rgba(236, 72, 153, 0.5)'
            } 0%, transparent 70%)`,
            animation: 'float 6s ease-in-out infinite reverse'
          }}
        />
      </div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center justify-start min-h-screen px-4 pt-20 pb-8">
        <div className="text-center mb-12 mt-2">
          <h1 className={`text-4xl md:text-5xl font-light tracking-wide mb-2 transition-colors duration-700 ${
            isDarkMode ? 'text-white' : 'text-gray-900'
          }`}>
            {cycling
              ? (currentHeading === 'naval' && 'Ask Naval')
                || (currentHeading === 'peter' && 'Ask Peter')
                || (currentHeading === 'paul' && 'Ask Paul')
                || (currentHeading === 'sama' && 'Ask Sama')
                || (currentHeading === 'charlie' && 'Ask Charlie')
              : (personality === 'naval' && 'Asking Naval')
                || (personality === 'peter' && 'Asking Peter')
                || (personality === 'paul' && 'Asking Paul')
                || (personality === 'sama' && 'Asking Sama')
                || (personality === 'charlie' && 'Asking Charlie')
            }
          </h1>
          <div className={`w-16 h-px bg-gradient-to-r mx-auto transition-all duration-700 ${
            isDarkMode 
              ? 'from-transparent via-gray-600 to-transparent' 
              : 'from-transparent via-gray-300 to-transparent'
          } ${cycling ? 'mt-0 mb-0' : 'mt-4 mb-0'}`}></div>
        </div>

        {/* Search container */}
        <div className="w-full max-w-2xl cursor-default" onClick={handleSearchClick}>
          <form onSubmit={handleSubmit} className="relative group">
            <div className={`absolute inset-0 rounded-2xl blur-sm opacity-0 group-hover:opacity-100 transition-all duration-500 ${
              isDarkMode 
                ? 'bg-gradient-to-r from-purple-500/10 via-blue-500/10 to-pink-500/10' 
                : 'bg-gradient-to-r from-purple-100/20 via-blue-100/20 to-pink-100/20'
            }`}></div>
            
            <div className={`relative backdrop-blur-sm rounded-2xl p-1.5 shadow-sm hover:shadow-md transition-all duration-300 ${
              isDarkMode 
                ? 'bg-gray-800/40 border border-gray-700/30 hover:bg-gray-800/50' 
                : 'bg-gray-50/40 border border-gray-200/30'
            }`}>
              <div className="flex items-center">
                <div className="flex-1 relative">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="i'll try not to yap too much"
                    className={`w-full bg-transparent px-6 py-4 text-lg font-light focus:outline-none transition-colors duration-300 ${
                      isDarkMode 
                        ? 'text-gray-200 placeholder-gray-500' 
                        : 'text-gray-700 placeholder-gray-400'
                    }`}
                    onKeyDown={handleKeyPress}
                    disabled={isLoading}
                  />
                </div>
                <button 
                  type="submit"
                  disabled={isLoading}
                  className={`flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 group-hover:scale-105 mr-2 ${
                    isDarkMode 
                      ? 'bg-gray-700/20 hover:bg-gray-700/30' 
                      : 'bg-gray-900/10 hover:bg-gray-900/20'
                  } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  <Search size={20} className={`transition-colors duration-300 ${
                    isDarkMode ? 'text-gray-400' : 'text-gray-600'
                  }`} />
                </button>
              </div>
            </div>
          </form>
          
          {/* Subtle hint text */}
          <p className={`text-center text-sm mt-6 font-light transition-colors duration-700 ${
            isDarkMode ? 'text-gray-500' : 'text-gray-400'
          }`}>
            just press enter or click the icon
          </p>
        </div>

        {/* Response section */}
        {isLoading && (
          <div className="w-full max-w-2xl mt-8">
            <div className={`text-center ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              <div className="animate-pulse">thinking...</div>
            </div>
          </div>
        )}

        {response && !isLoading && (
          <div className="w-full max-w-2xl mt-8" onClick={e => e.stopPropagation()}>
            <div className={`backdrop-blur-sm rounded-2xl p-6 shadow-sm transition-all duration-300 ${
              isDarkMode 
                ? 'bg-gray-800/40 border border-gray-700/30' 
                : 'bg-gray-50/40 border border-gray-200/30'
            }`}>
              <div className={`text-lg font-light leading-relaxed ${
                isDarkMode ? 'text-gray-200' : 'text-gray-700'
              }`}>
                {response}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Email Slide-in Panel (Bottom Right) */}
      {showEmailPopup && (
        <div
          className={`fixed z-50 bottom-6 right-6 w-[320px] max-w-xs
            ${showEmailPopup && !isClosingEmailBox ? 'email-expand-anim' : ''}
            ${isClosingEmailBox ? 'email-vacuum-anim' : ''}`}
          style={{ pointerEvents: isClosingEmailBox ? 'none' : 'auto' }}
          onClick={e => e.stopPropagation()}
        >
          <div className={`rounded-2xl shadow-xl p-4 flex flex-col items-center glassy-email-box relative transition-all duration-500 ${isClosingEmailBox ? 'opacity-0 scale-50' : ''}`}
            style={{boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.15)'}}>
            <div
              className={`text-sm font-light mb-2 text-center transition-colors duration-300 ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}
              style={isDarkMode
                ? { textShadow: '0 1px 4px rgba(0,0,0,0.25)' }
                : { textShadow: '0 1px 4px rgba(255,255,255,0.7)' }
              }
            >
              email? – personalize convos (beta)
            </div>
            <form onSubmit={handleEmailSubmit} className="w-full flex flex-col items-center">
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="your@email.com"
                className={`w-full px-3 py-1.5 rounded-lg shadow-sm
                  ${isDarkMode
                    ? 'bg-gray-800/60 text-gray-100'
                    : 'bg-gray-50/60 text-gray-900'}
                  focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm mb-2 transition`}
                required
                autoFocus
              />
              <button
                type="submit"
                className={`px-3 py-1 rounded-lg font-medium text-xs shadow-sm hover:opacity-90 transition
                  ${isDarkMode ? 'bg-white text-gray-900' : 'bg-gray-900 text-white'}`}
              >
                submit
              </button>
            </form>
            {/* Dash icon at bottom right */}
            <button
              className={`absolute bottom-2 right-2 w-8 h-8 flex items-center justify-center transition-all duration-500
                ${isClosingEmailBox ? 'email-vacuum-minus' : 'hover:bg-black/10 dark:hover:bg-white/10'}`}
              aria-label="Close email box"
              onClick={() => {
                setIsClosingEmailBox(true);
                setTimeout(() => {
                  setShowEmailPopup(false);
                  setIsClosingEmailBox(false);
                }, 600);
              }}
              type="button"
              tabIndex={0}
              style={isClosingEmailBox ? {pointerEvents: 'none', background: 'none', border: 'none'} : {background: 'none', border: 'none'}}
            >
              <span className="text-2xl text-gray-400 dark:text-gray-500 font-bold" style={{lineHeight: 1}}>-</span>
            </button>
          </div>
        </div>
      )}

      {(!showEmailPopup) && (
        <button
          className="fixed z-40 bottom-6 right-6 w-8 h-8 flex items-center justify-center transition-all duration-500"
          style={{background: 'none', border: 'none', boxShadow: 'none'}}
          aria-label="Open email box"
          tabIndex={0}
          onClick={e => { e.stopPropagation(); setShowEmailPopup(true); }}
        >
          <span className="text-2xl text-gray-400 dark:text-gray-500 font-bold" style={{lineHeight: 1}}>-</span>
        </button>
      )}

      {/* Invisible Side Panel with Profile Pictures */}
      <div className="fixed top-1/2 left-0 z-40 flex flex-col items-center gap-8 -translate-y-1/2 pl-2 pr-4 select-none" style={{pointerEvents: 'auto'}}>
        {profiles.map(profile => (
          <div key={profile.key} className="relative flex flex-col items-center group">
            <img
              src={profile.img}
              alt={profile.first}
              className={`w-12 h-12 rounded-full object-cover shadow-md cursor-pointer filter grayscale profile-pic-transition border-none border-0`}
              onMouseEnter={() => setHoveredProfile(profile.key)}
              onMouseLeave={() => setHoveredProfile(null)}
              onClick={() => { setPersonality(profile.key); setCycling(false); }}
              style={{background: '#eee', border: 'none'}}
            />
            {/* Name always visible for selected, else on hover */}
            <div
              className={`absolute left-14 top-1/2 -translate-y-1/2 flex flex-col items-start
                transition-all duration-300
                ${(hoveredProfile === profile.key || (!cycling && personality === profile.key)) ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-6 pointer-events-none'}`}
              style={{minWidth: '120px'}}
            >
              <span className="flex flex-col items-start">
                <span className="lowercase text-gray-500 font-semibold" style={{fontSize: '1.25rem', lineHeight: 1}}>{profile.first}</span>
                <span className="lowercase text-gray-400 font-normal text-xs" style={{fontSize: '0.92rem', lineHeight: 1}}>{profile.last}</span>
              </span>
              {/* Underline/border on hover or selected */}
              <span className={`block w-full h-0.5 mt-1 bg-gradient-to-r from-gray-300 to-gray-100 rounded transition-all duration-300
                ${(hoveredProfile === profile.key || (!cycling && personality === profile.key)) ? 'opacity-100 scale-x-100' : 'opacity-0 scale-x-0'}`}></span>
            </div>
          </div>
        ))}
      </div>

      <style>{`
         .email-vacuum-minus {
           animation: minusDrop 0.5s cubic-bezier(0.4,0,0.2,1) forwards;
         }
         @keyframes vacuum {
           0% {
             opacity: 1;
             transform: scale(1) translate(0, 0) skew(0deg, 0deg);
           }
           60% {
             opacity: 0.7;
             transform: scale(0.5) translate(80px, 0px) skew(-8deg, 2deg);
           }
           100% {
             opacity: 0;
             transform: scale(0.2) translate(140px, 80px) skew(-16deg, 4deg);
           }
         }
         .email-vacuum-anim {
           animation: vacuum 0.7s cubic-bezier(0.4,0,0.2,1) forwards;
         }
         @keyframes emailExpand {
           0% {
             opacity: 0.3;
             transform: scale(0.4) translate(140px, 80px) skew(-16deg, 4deg);
           }
           40% {
             opacity: 0.7;
             transform: scale(0.7) translate(80px, 0px) skew(-8deg, 2deg);
           }
           100% {
             opacity: 1;
             transform: scale(1) translate(0, 0) skew(0deg, 0deg);
           }
         }
         .email-expand-anim {
           animation: emailExpand 0.5s cubic-bezier(0.4,0,0.2,1);
         }
         .profile-pic-transition {
           transition: filter 0.5s, brightness 0.5s;
         }
         .dark .profile-pic-transition {
           filter: grayscale(1) brightness(0.85);
         }
         .profile-pic-transition {
           filter: grayscale(1) brightness(1);
         }
        `}</style>
    </div>
  );
}

export default App;
