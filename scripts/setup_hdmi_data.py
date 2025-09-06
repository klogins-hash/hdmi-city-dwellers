#!/usr/bin/env python3
"""
Setup HDMI City Dwellers sample data for the knowledge base
"""
import requests
import json
import time

def main():
    base_url = "http://localhost:8000"
    
    # Sample knowledge entries for HDMI City Dwellers
    sample_entries = [
        {
            "title": "HDMI 2.1 Technology",
            "content": "HDMI 2.1 is the latest HDMI standard supporting up to 48Gbps bandwidth, enabling 8K@60Hz and 4K@120Hz video transmission. Essential for modern urban displays and smart city infrastructure.",
            "category": "technology"
        },
        {
            "title": "Smart City Display Networks",
            "content": "Urban environments increasingly rely on interconnected display systems for information dissemination, emergency alerts, and public engagement. HDMI infrastructure forms the backbone of these networks.",
            "category": "smart-city"
        },
        {
            "title": "Urban Digital Signage",
            "content": "Digital signage in cities uses HDMI connections for high-quality content delivery to public displays, advertising boards, and information kiosks throughout urban environments.",
            "category": "infrastructure"
        },
        {
            "title": "City Traffic Management Systems",
            "content": "Modern traffic control centers use HDMI-connected displays for real-time monitoring of traffic flow, incident management, and coordination of smart traffic signals across urban networks.",
            "category": "urban-planning"
        },
        {
            "title": "Public Transportation Displays",
            "content": "Bus stops, train stations, and transit hubs utilize HDMI-powered displays for real-time arrival information, route updates, and passenger communication in smart city ecosystems.",
            "category": "connectivity"
        },
        {
            "title": "Emergency Response Systems",
            "content": "City emergency operations centers rely on HDMI display walls for coordinating responses to incidents, monitoring security cameras, and managing communication during crises.",
            "category": "infrastructure"
        },
        {
            "title": "Urban Data Visualization",
            "content": "City planners and administrators use HDMI-connected displays for visualizing urban data, population flows, energy consumption, and environmental monitoring in real-time dashboards.",
            "category": "smart-city"
        },
        {
            "title": "Fiber Optic HDMI Solutions",
            "content": "Long-distance HDMI transmission in cities uses fiber optic cables to maintain signal quality across large urban installations, supporting distributed display networks.",
            "category": "technology"
        },
        {
            "title": "Interactive City Kiosks",
            "content": "Public information kiosks throughout cities use HDMI connections to deliver interactive content, wayfinding assistance, and municipal services to residents and visitors.",
            "category": "connectivity"
        },
        {
            "title": "Smart Building Integration",
            "content": "Modern urban buildings integrate HDMI systems for conference rooms, lobbies, and collaborative spaces, supporting the connected city ecosystem and remote work infrastructure.",
            "category": "infrastructure"
        }
    ]
    
    print("Adding HDMI City Dwellers sample knowledge entries...")
    
    for entry in sample_entries:
        try:
            # Use the chat API to add entries
            message = f"add: {entry['title']} | {entry['content']} | {entry['category']}"
            
            response = requests.post(f"{base_url}/api/chat", json={
                "message": message,
                "session_id": "setup"
            })
            
            if response.status_code == 200:
                result = response.json()
                if result.get('data_modified'):
                    print(f"✅ Added: {entry['title']}")
                else:
                    print(f"❌ Failed to add: {entry['title']}")
            else:
                print(f"❌ HTTP Error for {entry['title']}: {response.status_code}")
                
            time.sleep(0.5)  # Small delay between requests
            
        except Exception as e:
            print(f"❌ Error adding {entry['title']}: {e}")
    
    print("\nHDMI City Dwellers setup complete! Try these test queries:")
    print("• 'What is HDMI 2.1?'")
    print("• 'Tell me about smart city displays'")
    print("• 'list technology'")
    print("• 'list smart-city'")
    print("• 'stats'")

if __name__ == "__main__":
    main()
