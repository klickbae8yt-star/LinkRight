# **The Open-Source AI Meeting and Interview Assistant Ecosystem: A Technical Analysis of Alternatives to Cluely**

## **Executive Summary**

The rapid expansion of the real-time AI desktop assistant market is driven by user demands for privacy-first, cost-effective meeting and interview copilots1. Commercial pioneers in this domain, most notably Cluely, established the viability of overlaying real-time automated transcription, screenshot analysis, and context-aware suggestions during live video calls, client presentations, and technical assessments2. However, the commercial landscape has been severely constrained by expensive subscription models—often exceeding $149 per month for advanced features like screen-share invisibility2—and significant security failures, such as the mid-2025 Cluely data breach that compromised the personal information, transcripts, and screen captures of 83,000 active users1.  
These challenges have accelerated the growth of a robust, highly active open-source ecosystem1. This research identifies and evaluates 14 distinct open-source projects developed to serve as technical alternatives to Cluely6. This ecosystem is undergoing a major transition from heavy, resource-intensive Electron-based wrappers to highly optimized Tauri/Rust frameworks and native macOS Swift applications10. This architectural shift reduces memory overhead and improves transcription latency1.  
The primary trends observed in this ecosystem center on the integration of "Bring Your Own Key" (BYOK) cloud APIs with localized, offline-first processing models1. These systems utilize optimized Small Language Models (SLMs) and hardware-accelerated speech-to-text engines to ensure complete data security1. Furthermore, anti-detection methodologies have evolved from basic transparent window styling to operating system compositor exclusions, such as Apple's native AppKit window management, which prevent any screen sharing or recording tools from capturing the assistant overlay10.

## **Complete Project Inventory**

The following table catalogs the 14 open-source projects identified as alternatives to Cluely, along with their key licensing, platform, model compatibility, and community metrics.

| Project Name | GitHub Repository | License | Platform | LLM Support | Stars | Last Commit | Key Differentiator |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Natively** | Natively-AI-assistant/natively-cluely-ai-assistant \[cite: 1\] | AGPL-3.016 | macOS, Windows1 | OpenAI, Anthropic, Gemini, local Ollama1 | \~1,50019 | May 202620 | Feature-complete Cluely clone with Phone Link companion and TinyPrompts SLM engine14. |
| **Pluely** | iamsrikanthnani/pluely \[cite: 22\] | GPL-3.023 | macOS, Windows, Linux11 | OpenAI, Anthropic, Gemini, Grok, Ollama11 | \~90022 | January 202622 | \~10MB Tauri build with dynamic custom cURL integrations and custom variable mapping11. |
| **Ghostbar** | rbc33/Ghostbar \[cite: 10\] | MIT10 | macOS (Native)10 | Ollama, OpenAI, Claude, OpenRouter, NIM10 | \~5625 | May 202626 | \~5MB native Swift application using sharingType \= .none compositor bypass10. |
| **OpenCluely** | TechyCSR/OpenCluely \[cite: 27\] | Apache-2.027 | macOS, Windows, Linux27 | Google Gemini27 | \~32927 | May 202627 | Draggable glass-morphism overlay with automatic local virtualenv Whisper integration27. |
| **Project Raven** | Laxcorp-Research/project-raven \[cite: 29\] | Custom29 | macOS, Windows29 | Claude, OpenAI29 | N/A | Early 202629 | Native WebRTC AEC3 echo cancellation isolating system audio from local microphone inputs29. |
| **Pikabaka** | royisme/pikabaka \[cite: 30\] | MIT31 | macOS, Windows30 | Gemini, OpenAI, Claude, Ollama30 | 032 | May 202630 | Sub-500ms real-time audio pipeline using sqlite-vec hybrid semantic search30. |
| **Unseen** | repowise-dev/unseen \[cite: 34\] | MIT34 | Cross-platform34 | YAML-mapped LLMs7 | 334 | May 202634 | YAML profile-driven assistant built on Repowise codebase intelligence architecture7. |
| **Clonely** | tahahah/Clonely \[cite: 35\] | MIT35 | Windows35 | Google Gemini35 | 1335 | July 202535 | Windows-centric clone developed to resolve rendering anomalies on Microsoft platforms35. |
| **Cass** | jadenpxrk/Cass \[cite: 6\] | MIT6 | macOS, Windows6 | Google Gemini6 | 116 | Late 20256 | Draggable Electron overlay capturing system audio and mic via Web Audio APIs6. |
| **MindWhisper AI** | SaimNadeemdev/MindWhisperAI-Cluely-Free-Alternative \[cite: 36\] | Custom37 | Windows37 | GPT, Claude, Gemini, Ollama37 | 3736 | January 202637 | Native Windows installer with a dual-mode free tier and commercial subscription37. |
| **Vysper** | varun-singhh/Vysper \[cite: 38\] | Apache-2.039 | macOS, Windows, Linux38 | Google Gemini38 | N/A | November 202538 | 9 structural domain-specific meeting skills panels using Tesseract OCR and Sox38. |
| **MeetingBro** | armpro24-blip/MeetingBro \[cite: 7\] | Custom | macOS, Windows | Local/Cloud models7 | N/A | Early 2026 | Local-first translation and diarization7. |
| **Vexa** | Vexa-ai/vexa \[cite: 8\] | Apache-2.08 | Linux (Self-hosted)8 | Webhook API models8 | \~2,20042 | Early 20268 | Headless, self-hosted meeting bot API with K8s deployment and native MCP tools8. |
| **Phantom Lens** | inulute/phantom-lens \[cite: 9\] | GPL-3.09 | Windows9 | Gemini9 | 1159 | December 20259 | Keyboard-driven overlay designed to minimize visual footprints during assessments9. |

## **Detailed Project Profiles**

### **Natively**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, TypeScript, Rust native node-addons1 |
| **Platform Compatibility** | macOS 12+ (Intel & Apple Silicon), Windows 10/111 |
| **Installation Rating** | Moderate (Offers pre-built installers alongside source builds)14 |
| **Primary Limitations** | High runtime memory consumption (\~150MB RAM) due to Electron dependencies10 |

#### **Architecture and Functional Analysis**

Natively is designed as a direct open-source clone of Cluely's frontend, but it introduces an entirely local execution pipeline to prevent cloud-based data exposure1. Developed by a single engineer in Kochi, India, the application uses a dual-channel audio engine1. This engine routes speaker system loopback audio and hardware microphone input to separate processing threads1. This segregation ensures that transcription remains clean even in noisy environments or during simultaneous conversations1.  
The software supports multiple speech-to-text models running entirely on-device, including Moonshine (tiny and base formats) and Whisper-large-v3-turbo1. These run through optimized ONNX engines that leverage local hardware acceleration, such as Apple's CoreML/Metal GPU and Windows DirectML1.

┌────────────────────────────────────────────────────────┐  
│                        Natively                        │  
│             (AGPL-3.0, Electron/React/Rust)             │  
└───────────────────────────┬────────────────────────────┘  
                            │  
              ┌─────────────┴─────────────┐  
              ▼                           ▼  
 ┌─────────────────────────┐ ┌─────────────────────────┐  
 │   On-Device ASR Core    │ │  Dual-Channel Audio     │  
 │ (ONNX Moonshine/Whisper)│ │   (System vs. Mic)      │  
 └────────────┬────────────┘ └────────────┬────────────┘  
              │                           │  
              └─────────────┬─────────────┘  
                            ▼  
 ┌─────────────────────────────────────────────────────┐  
 │                TinyPrompts™ Engine                  │  
 │    \- Context Compression (\<800 token payloads)      │  
 │    \- Optimized for Local SLMs (Qwen 2.5 / Llama 3.2) │  
 └──────────────────────────┬──────────────────────────┘  
                            │  
              ┌─────────────┴─────────────┐  
              ▼                           ▼  
 ┌─────────────────────────┐ ┌─────────────────────────┐  
 │  Stealth Window Engine  │ │  Phone Link Companion   │  
 │   (Process Disguise,    │ │ (Wireless Mic/Secondary │  
 │  Activity Monitor Mask) │ │   Display Execution)    │  
 └─────────────────────────┘ └─────────────────────────┘

Natively integrates a TinyPrompts™ engine, which compresses context sizes below 800 tokens by stripping XML structures14. This enables highly efficient reasoning on local Small Language Models (SLMs) like Qwen 2.5:4B and Llama 3.214.  
Additionally, the application supports Phone Link companion integration14. This feature lets users connect an external iOS or Android device over local WebSockets to act as a wireless microphone or secondary display14. This allows users to keep transcription text and suggestions completely off the primary computer monitor, mitigating the risk of detection during screen shares14.

### **Pluely**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Tauri, Rust core, React frontend11 |
| **Platform Compatibility** | macOS (Intel & Apple Silicon), Windows x64, Linux (Debian/RPM)11 |
| **Installation Rating** | Simple (Direct binary downloads available across major operating systems)11 |
| **Primary Limitations** | Transitioned to a freemium model with core features behind a paywall24 |

#### **Architecture and Functional Analysis**

Pluely is a highly optimized, cross-platform alternative designed to address the resource bottlenecks of Electron-based apps11. Built with Tauri and Rust, the final compiled application package is exceptionally compact at \~10MB11. By using native system web views (WKWebView on macOS, WebView2 on Windows) instead of bundling a full Chromium engine, Pluely reduces memory consumption to a fraction of the footprint typical of Electron apps10.  
The application features a translucent, click-through overlay window designed to stay hidden during active screen-sharing sessions11. It integrates customizable global hotkeys (such as Cmd+\\ for window toggles and Cmd+Shift+M for system audio capture)11.  
A key technical feature is its custom API integration11. Instead of using hardcoded API wrappers, users can input raw cURL execution statements11. Pluely dynamically maps placeholder parameters—such as {{TEXT}} or {{IMAGE}}—into these statements, allowing users to route data to any proprietary cloud or local LLM endpoint without storing API keys on external servers11.

┌────────────────────────────────────────────────────────┐  
│                         Pluely                         │  
│               (GPL-3.0, Tauri/Rust/React)              │  
└───────────────────────────┬────────────────────────────┘  
                            │  
              ┌─────────────┴─────────────┐  
              ▼                           ▼  
 ┌─────────────────────────┐ ┌─────────────────────────┐  
 │      Tauri Core         │ │     Custom Intercept    │  
 │ (Lightweight \~10MB Bin) │ │   (Direct cURL Pipe)    │  
 └────────────┬────────────┘ └────────────┬────────────┘  
              │                           │  
              └─────────────┬─────────────┘  
                            ▼  
 ┌─────────────────────────────────────────────────────┐  
 │                Stealth Control Unit                 │  
 │      \- Translucent Screen Overlay Window            │  
 │      \- Adaptive Cursor Masking (Invisible/Auto)      │  
 └─────────────────────────────────────────────────────┘

However, Pluely's development trajectory changed in late 2025 and early 202624. The developer transitioned the main real-time audio and meeting assistance capabilities behind a $120 premium commercial license24. This transition has made the free, open-source version of the repository largely static24.

### **Ghostbar**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Native Swift, AppKit window rendering libraries10 |
| **Platform Compatibility** | macOS 13+ (Native)10 |
| **Installation Rating** | Simple (Available via fast Homebrew cask installs or standalone DMG)10 |
| **Primary Limitations** | Completely incompatible with Windows and Linux operating systems10 |

#### **Architecture and Functional Analysis**

Ghostbar is a minimalist macOS menu bar application designed specifically to bypass the system display compositor10. Developed in native Swift, it avoids the performance overhead of bundled browser runtimes, resulting in an application size of \~5MB and idle memory utilization of under 30MB10.

┌────────────────────────────────────────────────────────┐  
│                        Ghostbar                        │  
│               (MIT, Swift/AppKit Native)               │  
└───────────────────────────┬────────────────────────────┘  
                            │  
              ┌─────────────┴─────────────┐  
              ▼                           ▼  
 ┌─────────────────────────┐ ┌─────────────────────────┐  
 │   Swift / AppKit Core   │ │   Compositor Bypass     │  
 │  (\~5MB Execution Size)  │ │ (sharingType \= .none)   │  
 └────────────┬────────────┘ └────────────┬────────────┘  
              │                           │  
              └─────────────┬─────────────┘  
                            ▼  
 ┌─────────────────────────────────────────────────────┐  
 │                On-Device Inference                  │  
 │      \- On-Device Whisper (via whisper.cpp)          │  
 │      \- MLX-Optimized Local LLM Execution            │  
 └─────────────────────────────────────────────────────┘

Ghostbar's primary technical differentiator is its use of macOS's native AppKit window management API10. By setting the parameter window.sharingType \= .none, the application instructs the macOS window server to exclude the window surface from the display's video capture pipeline10. As a result, the overlay renders normally on the user's physical display but appears completely invisible to screen sharing and recording tools like Zoom, Microsoft Teams, OBS Studio, and Apple's native screen capture tools10.  
Ghostbar also prioritizes local, private processing10. It includes built-in, on-device transcription using a C++ port of Whisper (whisper-cpp) and supports hardware-accelerated local models via Apple Silicon MLX bindings10. This architectural approach ensures that sensitive data never leaves the user's machine10.

### **OpenCluely**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, integrated Python Whisper virtual environments27 |
| **Platform Compatibility** | macOS, Windows, Linux27 |
| **Installation Rating** | Simple (Provides an automated installation script)27 |
| **Primary Limitations** | Features are highly tailored for technical interviews, limiting general meeting use7 |

#### **Architecture and Functional Analysis**

OpenCluely is a specialized open-source fork of the Vysper assistant, designed specifically for technical software engineering interviews, online coding assessments, and competitive programming27. The application uses an Electron platform and features a translucent, glass-morphic command bar overlay that remains always-on-top while supporting click-through interactions27. This lets users interact with background development environments or text editors directly through the overlay window27.  
A key aspect of OpenCluely is its automated setup architecture27. Running ./setup.sh automatically installs system dependencies, configures the environment file, builds the codebase, and creates a localized Python virtual environment (.venv-whisper) that points directly to an offline Whisper installation27. This eliminates the need for manual NPM builds or complex virtual environment setup27.  
Additionally, the application uses basic process-masking methods to hide its presence27. It alters its process identifiers to masquerade as standard system utilities (such as Activity Monitor, Settings, or Terminal) in task lists, helping it evade detection by monitoring tools27.

### **Project Raven**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, native GStreamer interfaces, WebRTC AEC3 plugins29 |
| **Platform Compatibility** | macOS 12+ (Intel & Apple Silicon), Windows 10/1129 |
| **Installation Rating** | Advanced (Requires manual compilation of native packages and tools)29 |
| **Primary Limitations** | Complex, multi-step installation makes it inaccessible to non-technical users29 |

#### **Architecture and Functional Analysis**

Project Raven is a technical framework designed to solve a major hardware limitation of real-time meeting assistants: acoustic loopback bleed29. Built on Electron, the application routes active capture streams through native GStreamer pipelines29. These are compiled directly on the user's machine using custom node-gyp and cmake-js processes29.  
To prevent transcription errors caused by speaker output bleeding back into the microphone, Project Raven integrates WebRTC's advanced AEC3 (Acoustic Echo Cancellation) engine29. The software captures system output and microphone input on separate channels, modeling the physical room acoustics to subtract the speaker's voice from the microphone feed in real time29. This processes clean, isolated audio streams for transcription29.  
However, the application requires an exceptionally complex installation process29. Users must manually configure Xcode Command Line Tools or Visual Studio Build Tools, install local Python and Rust compiler chains, download platform-specific GStreamer runtimes, and compile native C++ add-ons targeting the specific Electron version29. This high technical barrier limits its adoption to advanced developers and system engineers29.

### **Pikabaka**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, Rust, node-addon-api, sqlite-vec indexers30 |
| **Platform Compatibility** | macOS, Windows30 |
| **Installation Rating** | Moderate (Requires compiling Rust node-addons from source)30 |
| **Primary Limitations** | Minimal GUI documentation and low initial community adoption32 |

#### **Architecture and Functional Analysis**

Pikabaka is an open-source assistant designed for ultra-low latency speech transcription30. Developed in TypeScript, it integrates a high-performance audio engine written in Rust using Node-API bindings (napi-rs)30. This architecture bypasses standard Web Audio constraints to capture and process system signals with sub-500ms latency1.  
A key technical feature is its localized vector search architecture30. Pikabaka uses sqlite-vec to run a hybrid search database (combining BM25 keyword matching with vector embeddings) entirely on-device30. During a live meeting, the system embeds transcribed text dynamically and queries this database to retrieve relevant reference materials, such as documentation or coding solutions, in real time30.  
The interface is minimalist, designed to overlay active screens without drawing attention30. However, the project's complex dependencies—such as compiling native Rust extensions during installation—and a lack of comprehensive documentation have limited its adoption within the developer community30.

### **Unseen**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | TypeScript, Repowise AST indexing layers34 |
| **Platform Compatibility** | Cross-platform34 |
| **Installation Rating** | Simple (Runs via standard node commands or NPM executions)34 |
| **Primary Limitations** | Lacks a graphical overlay window, relying instead on terminal displays34 |

#### **Architecture and Functional Analysis**

Unseen is an open-source meeting copilot developed by the Repowise organization7. Rather than functioning as a traditional screen-overlay tool, the application serves as a developer-focused assistant integrated with Repowise's broader codebase intelligence architecture34.  
The tool leverages YAML-configured profiles to customize the assistant's behavior based on meeting types, such as architecture reviews, daily standups, or system design interviews7. Because it is designed to pair with the Repowise ecosystem, it can ingest live meeting transcripts and cross-reference them with its structural indexes, git histories, and developer wikis34. This architecture lets the underlying AI model resolve contextual queries (e.g., explaining why a specific database pattern was chosen) based on live conversation34.  
While highly powerful for engineering teams, Unseen lacks a traditional translucent graphical overlay34. Instead, it uses terminal-based feedback and dashboard interfaces, making it less suitable for users looking for an invisible Cluely-style desktop assistant34.

### **Clonely**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, Vite, TypeScript, Gemini API wrappers35 |
| **Platform Compatibility** | Windows-optimized35 |
| **Installation Rating** | Simple (Requires standard cloning and basic NPM package installations)35 |
| **Primary Limitations** | Features are hardcoded to Google Gemini models, lacking multi-backend support35 |

#### **Architecture and Functional Analysis**

Clonely was developed by software engineer tahahah to address UI rendering and performance issues when running Cluely on Windows platforms35. Built on Electron and Vite, the codebase is highly optimized for the Windows desktop manager, ensuring smooth rendering of translucent overlays35.  
The application supports two primary operational modes: an on-demand chat mode and a continuous live voice mode35. In chat mode, the user types prompts via global keyboard shortcuts (Ctrl+Enter), triggering screen captures that are sent with the prompt to the AI model35. In voice mode, the application continuously records system audio and microphone inputs, streaming the content to generate real-time suggestions35.  
To manage visibility, the application maps global keyboard shortcuts (Ctrl+Space) to instantly toggle overlay transparency, making it easy to hide the interface during live presentations35. However, Clonely is hardcoded to Google Gemini APIs, meaning users must provide a Gemini API key and cannot route queries to other backends like Anthropic Claude, OpenAI, or local Ollama setups35.

### **Cass**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, Web Audio APIs, Gemini API integrations6 |
| **Platform Compatibility** | macOS, Windows6 |
| **Installation Rating** | Simple (Direct app bundle downloads available from repository releases)6 |
| **Primary Limitations** | Deprecated native screen-protection features, relying on third-party filters6 |

#### **Architecture and Functional Analysis**

Cass is a floating desktop assistant designed to provide a lightweight, draggable companion window for LeetCode exercises, math solutions, multiple-choice questions, and sales calls6. Built on Electron, the application maps screen captures and system audio streams to Google Gemini models via BYOK configurations6.  
The interface detects task types automatically and formats responses accordingly6. For example, programming queries return Markdown code fences with syntax highlighting, math problems show structured, step-by-step derivations, and multiple-choice questions display correct selections alongside explanations6.  
Earlier versions of Cass included native screen-protection drivers to hide the window from screen sharing software6. However, due to system stability issues on newer macOS versions, the developer removed these native drivers6. The application now behaves as a standard overlay, meaning its visibility during screen shares depends entirely on the video conferencing platform's native window filters6.

### **MindWhisper AI**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, Tailwind CSS, multi-backend integrations36 |
| **Platform Compatibility** | Windows 10/11 (Native .exe), with macOS and Linux plans pending37 |
| **Installation Rating** | Simple (Standard Windows setup executable)37 |
| **Primary Limitations** | Transitioning toward a paid subscription model37 |

#### **Architecture and Functional Analysis**

MindWhisper AI, released in January 2026, is a real-time meeting and interview assistant built on Electron37. It features sub-300ms transcription latency and supporting speech recognition across more than 50 languages37.  
The application supports multiple backend providers, allowing users to switch between cloud models (such as GPT-4o, Gemini 2.0, and Claude) and local Ollama deployments (such as Llama 3.2 or CodeLlama) for fully offline processing37. It includes draggable translucent overlays, visual screenshot processing, and global hotkeys to toggle visibility during calls37.  
While marketed as a free alternative to Cluely on GitHub, MindWhisper AI's releases include promotional structures for paid premium plans starting at $10 per month37. This indicating a transition from a purely open-source project to a commercial, freemium model37.

### **Vysper**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, Tesseract OCR, Sox binary dependencies38 |
| **Platform Compatibility** | macOS, Windows, Linux38 |
| **Installation Rating** | Advanced (Requires manual package installations via Homebrew/Chocolatey)38 |
| **Primary Limitations** | Project development has slowed, with the last major updates in late 20257 |

#### **Architecture and Functional Analysis**

Vysper is an AI-powered desktop companion designed specifically for professional and technical assessments38. Built on Electron, the system captures screen content using Tesseract OCR and processes microphone input using system-level Sox audio tools38.

┌────────────────────────────────────────────────────────┐  
│                        Vysper                          │  
│             (Apache-2.0, Electron/React)               │  
└───────────────────────────┬────────────────────────────┘  
                            │  
              ┌─────────────┴─────────────┐  
              ▼                           ▼  
 ┌─────────────────────────┐ ┌─────────────────────────┐  
 │      Tesseract OCR      │ │        Sox Audio        │  
 │  (Local Optical Engine) │ │  (System Capture Pip)   │  
 └────────────┬────────────┘ └────────────┬────────────┘  
              │                           │  
              └─────────────┬─────────────┘  
                            ▼  
 ┌─────────────────────────────────────────────────────┐  
 │                Modular Skills Panel                 │  
 │     \- DSA, System Design, behavioral, Sales, etc.   │  
 │     \- Custom prompt payloads tailored per mode      │  
 └─────────────────────────────────────────────────────┘

The application's key differentiator is its modular skills selector38. It provides 9 specialized domain-specific prompt profiles: Data Structures and Algorithms (DSA), System Design, Behavioral (STAR method), Sales, Negotiation, Presentation, DevOps, Data Science, and General Programming38. Each mode dynamically adjusts the underlying system prompt and OCR extraction parameters to deliver highly context-aware suggestions38.  
However, the installation process requires users to manually install Tesseract and Sox binaries using command-line package managers (like Homebrew on macOS or Chocolatey on Windows)38. Additionally, the codebase has seen decreased activity, with development slowing significantly after June 202547.

### **MeetingBro**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, localized Whisper translations7 |
| **Platform Compatibility** | macOS, Windows7 |
| **Installation Rating** | Simple (Standard node commands) |
| **Primary Limitations** | Limited stealth features, focusing primarily on raw translation workflows7 |

#### **Architecture and Functional Analysis**

MeetingBro is a local-first meeting transcription tool developed under the armpro24-blip organization7. Unlike stealth assistants designed to cheat on coding assessments, MeetingBro is built as a productivity tool for professional meetings, lectures, and live translations7.  
The application runs a localized transcription engine to process system and microphone audio inputs, generating real-time translations alongside the transcript7. Because it prioritizes local processing, it is highly optimized for privacy and data sovereignty, ensuring meeting logs are never sent to external servers7.  
However, the application lacks advanced stealth features, such as display compositor bypasses or process-masking mechanisms7. This makes it less suitable for users who require complete overlay invisibility during high-stakes evaluations or presentations7.

### **Vexa**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Go, TypeScript, GStreamer, Puppeteer headless web-browsers8 |
| **Platform Compatibility** | Linux (Docker, Helm, Kubernetes deploy-ready)8 |
| **Installation Rating** | Advanced (Requires complete container orchestration and hosting configuration)8 |
| **Primary Limitations** | No client-side GUI overlay; functions as a backend bot infrastructure8 |

#### **Architecture and Functional Analysis**

Vexa is an enterprise-grade, open-source meeting bot and transcription API designed to replace expensive SaaS integrations like Recall.ai or Otter.ai8. Written in Go and TypeScript, the system is deployed as a cluster of containerized microservices managed via Docker or Kubernetes8.  
Vexa deploys headless, automated browser instances (via Puppeteer/Chromium) directly into Google Meet, Microsoft Teams, and Zoom meetings8. These automated bots capture raw system audio and video streams, sending them to localized Whisper or Deepgram pipelines to generate real-time transcriptions via WebSocket endpoints8.

                                  ┌──────────────────┐  
                                  │   Target Call    │  
                                  │ (Meet/Teams/Zoom)│  
                                  └────────┬─────────┘  
                                           │  
                                           ▼  
┌──────────────────┐              ┌────────┴─────────┐  
│   Vexa API Hub   ├─────────────►│ Headless Bot     │  
│ (Go/K8s Cluster) │              │ (Puppeteer/Chrom)│  
└──────────────────┘              └────────┬─────────┘  
                                           │  
                                           ▼  
┌──────────────────┐              ┌────────┴─────────┐  
│  Local Database  │◄─────────────┤ ASR Pipeline     │  
│   (Postgres)     │              │ (Local Whisper)  │  
└──────────────────┘              └──────────────────┘

The system also integrates a native Model Context Protocol (MCP) server with 17 specialized tools, enabling AI agents to join calls, analyze transcripts, and interact with participants8. While highly scalable for organizational use, Vexa does not provide a desktop overlay, making it unsuitable as a personal, stealth interview copilot8.

### **Phantom Lens**

| Attribute | Profile Specification |
| :---- | :---- |
| **Framework & Core Tech** | Electron, React, custom screenshot OCR utilities9 |
| **Platform Compatibility** | Windows (Native executable available; macOS and Linux planned)9 |
| **Installation Rating** | Simple (Direct binary setup executable available)9 |
| **Primary Limitations** | Lacks automated speech-to-text; relies heavily on manual screenshot inputs9 |

#### **Architecture and Functional Analysis**

Phantom Lens is an open-source, keyboard-driven Cluely alternative built on Electron by developer inulute9. The codebase was heavily inspired by Cass, but it is optimized specifically to minimize its visual footprint during high-stakes exams and online assessments9.  
The application relies on a keyboard-driven workflow, allowing users to control all features via global hotkeys9. Pressing Ctrl+\\ toggles overlay visibility, while Ctrl+Enter captures the screen, runs OCR, and routes the content to the AI model9. Users can also reposition the window using Ctrl+Arrow Keys and toggle transparency using Ctrl+Shift+V9.  
By focusing on manual screenshot inputs rather than continuous background audio transcription, Phantom Lens maintains a very low resource footprint on Windows machines9. However, the lack of automated, real-time speech-to-text makes it less effective for dynamic, verbal meetings or interactive sales calls9.

## **Technical Comparison Matrices**

### **Table 1: Detailed Feature Analysis**

| Project Name | Transcription Latency | Stealth Capability | Local LLM Support | Screenshot OCR | Native RAG / Search | Echo Cancellation |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Natively** | \<500ms (Moonshine)1 | Process disguise, event blocking14 | Yes (Ollama)1 | Yes (Local ONNX)1 | Yes (Rolling context)1 | Yes (Dual-channel separation)1 |
| **Pluely** | \~1.2s (API dependent)24 | Translucent overlay11 | Yes (Custom endpoints)11 | Yes (Manual drag region)11 | No (Direct endpoint queries) | No (Direct hardware capture)24 |
| **Ghostbar** | \~800ms (whisper.cpp)10 | Compositor exclude (sharingType)10 | Yes (MLX local engine)15 | Yes (Capture hotkey)10 | No (Direct prompt memory) | No (Voice activity thresholds)10 |
| **OpenCluely** | \~1.5s (Python Whisper)27 | Draggable glass-morphic hide27 | No (Requires cloud Gemini)27 | Yes (Smart Image capture)27 | Yes (History contexts)27 | No (Raw system inputs) |
| **Project Raven** | \~600ms (Deepgram API)29 | Basic transparent overlay29 | No (Claude/OpenAI cloud)29 | No (Audio-only capture) | No (Direct meeting streams) | Yes (WebRTC AEC3 filter)29 |
| **Pikabaka** | \<500ms (Rust audio)30 | Basic transparent overlay30 | Yes (Ollama)30 | Yes (Vision analysis)30 | Yes (sqlite-vec hybrid database)30 | No (Raw hardware capture) |
| **Vexa** | \<300ms (Streaming API)8 | N/A (Headless backend)8 | Yes (Self-hosted pipelines)8 | No (API audio-only) | Yes (MCP agent tools)8 | Yes (Decoupled system audio)8 |
| **Phantom Lens** | N/A (Manual inputs)9 | Instant toggle hide, translucent9 | No (Gemini vision dependencies)9 | Yes (Hotkey area capture)9 | No (Direct task memory) | N/A (No audio capture)9 |

### **Table 2: AI Backend and Speech-to-Text Integrations**

| Project Name | Google Gemini | OpenAI API | Anthropic Claude | Local Ollama | Local Whisper | Azure Speech API |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Natively** | Yes18 | Yes1 | Yes1 | Yes1 | Yes (ONNX Moonshine/Whisper)1 | Yes18 |
| **Pluely** | Yes11 | Yes11 | Yes11 | Yes11 | Yes (ElevenLabs/Groq STT)11 | Yes (Custom cURL configurations)11 |
| **Ghostbar** | Yes (OpenRouter)10 | Yes10 | Yes10 | Yes10 | Yes (whisper-cpp)10 | Yes (NVIDIA NIM endpoints)10 |
| **OpenCluely** | Yes27 | No | No | No | Yes (Python Virtualenv)27 | Yes27 |
| **Project Raven** | No | Yes29 | Yes29 | No | No (Deepgram cloud STT)29 | No |
| **Pikabaka** | Yes30 | Yes30 | Yes30 | Yes30 | Yes (Rust native audio)30 | No |
| **Vexa** | No | Yes (API pipelines)8 | Yes (API pipelines)8 | Yes (Self-hosted models)8 | Yes48 | Yes (SaaS gateways)8 |
| **Phantom Lens** | Yes9 | No | No | No | No (No audio processing)9 | No |

## **Ecosystem and Community Analysis**

The development of open-source alternatives to Cluely is driven by two main factors: maintaining data privacy and bypassing expensive commercial subscription fees1. Natively is currently the most active community-led project in this space1. The repository has gained approximately 1,500 GitHub stars and maintains regular development cycles19. Its community discussions are highly active, focusing on optimizing local speech recognition and developing techniques to evade detection by monitoring software21.  
Another active project is OpenCluely, which has built a dedicated user base by focusing on technical programming assessments27.

                  ┌──────────────────────────────────┐  
                  │          varun-singhh/Vysper     │  
                  │   (Conceptual Domain Skills Mod) │  
                  └────────────────┬─────────────────┘  
                                   │  
                           Inspirational Fork  
                                   │  
                                   ▼  
                  ┌──────────────────────────────────┐  
                  │         TechyCSR/OpenCluely      │  
                  │   (DSA Technical Focus Overlay)  │  
                  └──────────────────────────────────┘

The ecosystem also contains several inactive or abandoned projects6. Clonely has not received updates since mid-2025, largely because its single-model (Gemini-only) design limits its versatility35. Similarly, Cass has deprecated its native screen-protection features, making it less effective as a stealth assistant6.  
Additionally, some projects have transitioned from open-source to commercial models24. Pluely, which began as an open-source Tauri project, monetized its core real-time audio capture features behind a paid license, leaving the public repository mostly inactive24. MindWhisper AI followed a similar path, introducing paid premium subscription structures alongside its initial public GitHub releases37.

## **Commercial Market Context and Pricing Dynamics**

Commercial real-time AI assistants target high-stress professional interactions, using marketing copy that promises "undetectable" performance to justify premium subscription fees2. However, analyzing their pricing structures reveals significant costs for features that open-source alternatives provide for free1.

| Commercial Competitor | Basic Monthly Plan | Premium / Stealth Plan | Key Limitations & Structural Risks |
| :---- | :---- | :---- | :---- |
| **Cluely** | $19.99/month2 | $149.99/month (Pro \+ Stealth)2 | Experienced a major security breach in mid-2025, exposing 83,000 users' logs and screen captures1. |
| **Final Round AI** | Free trial (highly limited)50 | $148.00/month5 | Features high transcription latency (\~4s) and visible background application icons5. |
| **Interview Sidekick** | Free demo (2-minute limit)50 | $40.00/month50 | Lacks advanced analytics and has a higher risk of being flagged by monitoring software50. |
| **HuddleMate** | N/A (Pay-per-minute model)51 | $14.99/hour51 | The cumulative hourly pricing model becomes expensive during extended usage or prep sessions51. |
| **Interviews.chat** | $19.00/month (Starter tier)50 | $29.00/month (Booster tier)50 | Relies on credit-based billing, limiting continuous real-time transcriptions50. |

These commercial tools use cloud-centric processing models, meaning all audio transcripts, screen captures, and user metadata are routed through and stored on their servers1. This architecture creates significant security vulnerabilities, as demonstrated by the mid-2025 Cluely data breach1.  
In contrast, open-source alternatives like Natively, Ghostbar, and OpenCluely run fully on-device1. This eliminates cloud-hosting risks and ongoing subscription fees, providing a more secure and cost-effective solution1.

## **Strategic Recommendations**

### **Best Overall Alternative: Natively**

Natively is the most comprehensive open-source alternative to Cluely, providing a polished interface, active development, and robust local execution features1.  
Its dual-channel audio separation and support for local ONNX speech engines allow it to deliver sub-500ms transcription latencies entirely offline1. This makes it highly effective for users who require a reliable, private, and feature-rich copilot on macOS or Windows1.

### **Best for Privacy and macOS Native Efficiency: Ghostbar**

Ghostbar is the recommended choice for macOS users who prioritize lightweight, system-native performance10. Written in pure Swift, the application uses only \~5MB of disk space and under 30MB of RAM, making it vastly more efficient than typical Electron-based apps10.  
Its use of Apple's AppKit display compositor exclusion (sharingType \= .none) provides highly reliable overlay invisibility during screen shares, making it an excellent tool for secure macOS workflows10.

### **Best for High-Performance Audio and WebRTC Filters: Project Raven**

For complex acoustic setups or environments with significant background noise, Project Raven provides the most advanced audio processing capabilities29.  
Its custom-compiled WebRTC AEC3 engine effectively filters out speaker feedback from the microphone channel29. While the manual installation process is highly complex, the resulting audio isolation makes it the most capable tool for managing complex, multi-speaker meetings29.

### **Best for Technical Interview Preparation: OpenCluely**

OpenCluely is highly optimized for technical software engineering interviews, competitive programming, and online assessments27.  
Its glass-morphism overlay supports full click-through interactions, allowing users to write and run code in their IDE directly through the overlay window27. The automated script-based virtual environment setup also makes it highly accessible for developers focused on technical interview prep27.

### **Best for Enterprise and Team Infrastructure: Vexa**

Vexa is the leading open-source choice for organizational deployments, corporate compliance, and team workflows8.  
Its self-hosted, containerized microservice architecture lets enterprises run headless meeting bots directly on their own cloud or on-premise servers8. This ensures complete data sovereignty and provides developers with robust, multi-tenant API controls and native Model Context Protocol (MCP) integrations8.

## **Gaps, Emerging Technologies, and Future Research Trajectories**

### **Operational Gaps and Proctoring Defenses**

While the open-source ecosystem provides robust tools for standard screen sharing and video conferencing software, a significant operational gap remains when encountering kernel-level proctoring and active monitoring systems3. Standard security engines (such as Pearson VUE, ProctorU, or Respondus) do not rely on basic screen-sharing APIs17. Instead, they run with administrative operating system privileges, allowing them to scan active process lists, verify window hierarchies, inspect driver signatures, and block unauthorized virtual audio loopbacks17.  
Most open-source assistants are built on Electron or Tauri frameworks1. These can be easily identified by process-monitoring tools due to their predictable system behaviors and dependency on underlying browser rendering runtimes10. Consequently, running these overlays on the host machine during proctored assessments carries a high risk of detection, regardless of compositor exclusion flags3.

### **Emerging Technologies and Decoupled Hardware Architectures**

To address these security and detection risks, developers are shifting toward hardware-decoupled architectures14. Natively's Phone Link companion integration is a key example of this approach14. By offloading transcription, suggestion rendering, and LLM queries to a secondary mobile device over local WebSockets, the host computer remains free of active overlays or background processes14.

┌────────────────────────────────────────────────────────┐  
│                      Host Machine                      │  
│            \- Standard, unmodified OS state             │  
│            \- Virtual loopback audio capture            │  
└───────────────────────────┬────────────────────────────┘  
                            │  
                  Local WebSocket Stream  
                            │  
                            ▼  
┌────────────────────────────────────────────────────────┐  
│                   Companion Mobile                     │  
│            \- Runs overlay and suggestions              │  
│            \- No traces on host screen capture          │  
└────────────────────────────────────────────────────────┘

Future development in this space is focusing on hardware-level video and audio interception14. For example, using physical HDMI pass-through capture cards (such as USB-C UVC capture dongles) combined with external microcontrollers (like a Raspberry Pi 5 running local Whisper and lightweight SLMs), the meeting's video and audio can be intercepted and analyzed completely externally. This hardware-isolated approach leaves zero process signatures, window handles, or driver modifications on the primary computer, making it virtually impossible for host-based proctoring software to detect.

### **Advancements in On-Device Speech Engines**

The viability of local-first meeting assistants is closely tied to ongoing optimization in speech-to-text models and Small Language Models1. Early versions of these tools relied on cloud APIs, which introduced high operational latency and data privacy risks1.  
The introduction of optimized local speech engines—such as ONNX-quantized Moonshine and whisper.cpp—allows modern computers to run high-accuracy transcription locally with sub-500ms latencies1.  
Let ![][image1] represent the input audio chunk duration, ![][image2] represent the localized inference time, and ![][image3] represent the language model's generation delay. The total system latency is defined as:  
![][image4]  
By reducing the audio segment processing window (![][image5]) and utilizing highly optimized, hardware-accelerated local SLMs, open-source projects can achieve system latencies where:  
![][image6]  
This provides users with immediate, context-aware suggestions during live, fast-paced conversations without relying on cloud servers or incurring subscription costs1.

#### **Works cited**

1. Natively — Free open-source AI meeting assistant, interview copilot, and note taker. The best alternative to Cluely, Otter, Granola, Final Round AI, Fireflies, and Interview Coder. Real-time transcription, AI meeting notes, lecture recording, local RAG, BYOK, and stealth mode. Runs locally. No subscriptions. No data breaches. · GitHub, [https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant)  
2. Honest Review of Cluely: The AI App That's Faking Your Meetings \- tl;dv, [https://tldv.io/blog/cluely-review/](https://tldv.io/blog/cluely-review/)  
3. Cluely AI Review: Everything You Need to Know in 2026 \- BitDegree.org, [https://www.bitdegree.org/ai/cluely-ai-review](https://www.bitdegree.org/ai/cluely-ai-review)  
4. Cluely Review: I Tested to See If it Suits for Interviews \- Linkjob AI, [https://www.linkjob.ai/hub/cluely-review/](https://www.linkjob.ai/hub/cluely-review/)  
5. Best AI copilot for interviews? Not GitHub Copilot \-- actual interview copilots : r/InterviewHackers \- Reddit, [https://www.reddit.com/r/InterviewHackers/comments/1rwiz18/best\_ai\_copilot\_for\_interviews\_not\_github\_copilot/](https://www.reddit.com/r/InterviewHackers/comments/1rwiz18/best_ai_copilot_for_interviews_not_github_copilot/)  
6. jadenpxrk/Cass: A clone of Cluely \- GitHub, [https://github.com/jadenpxrk/ikiag](https://github.com/jadenpxrk/ikiag)  
7. cluely · GitHub Topics, [https://github.com/topics/cluely?o=desc\&s=forks](https://github.com/topics/cluely?o=desc&s=forks)  
8. GitHub \- Vexa-ai/vexa: Open-source meeting transcription API for Google Meet, Microsoft Teams & Zoom. Auto-join bots, real-time WebSocket transcripts, MCP server for AI agents. Self-host or use hosted SaaS., [https://github.com/Vexa-ai/vexa](https://github.com/Vexa-ai/vexa)  
9. GitHub \- inulute/phantom-lens: A Cluely / Interview Coder alternative with features we probably shouldn't talk about, built for winning exams.., [https://github.com/inulute/phantom-lens](https://github.com/inulute/phantom-lens)  
10. GitHub \- rbc33/Ghostbar: Free macOS-native Cluely alternative. AI chat invisible to screen sharing. Ollama, OpenAI, Claude. Swift. No Electron. No subscription., [https://github.com/rbc33/Ghostbar](https://github.com/rbc33/Ghostbar)  
11. Pluely \- Invisible Open Source AI Assistant, [https://pluely.com/](https://pluely.com/)  
12. Show HN: Pluely – open-source alternative to Cluely (\~10MB, Always On Display) | Hacker News, [https://news.ycombinator.com/item?id=44949395](https://news.ycombinator.com/item?id=44949395)  
13. Free native macOS alternative to Cluely — open source, Ollama support, no subscription : r/cscareerquestionsOCE \- Reddit, [https://www.reddit.com/r/cscareerquestionsOCE/comments/1t3nbul/free\_native\_macos\_alternative\_to\_cluely\_open/](https://www.reddit.com/r/cscareerquestionsOCE/comments/1t3nbul/free_native_macos_alternative_to_cluely_open/)  
14. Releases · Natively-AI-assistant/natively-cluely-ai-assistant \- GitHub, [https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/releases](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/releases)  
15. I built a native Swift macOS AI client that's invisible to screen sharing — works with Ollama, vLLM, llama.cpp \[OC\] : r/LocalLLaMA \- Reddit, [https://www.reddit.com/r/LocalLLaMA/comments/1tgsro5/i\_built\_a\_native\_swift\_macos\_ai\_client\_thats/](https://www.reddit.com/r/LocalLLaMA/comments/1tgsro5/i_built_a_native_swift_macos_ai_client_thats/)  
16. natively-cluely-ai-assistant/LICENSE at main \- GitHub, [https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/blob/main/LICENSE](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/blob/main/LICENSE)  
17. natively-cluely-ai-assistant \- AI Agents on GitHub | SkillsLLM, [https://skillsllm.com/skill/natively-cluely-ai-assistant](https://skillsllm.com/skill/natively-cluely-ai-assistant)  
18. natively-cluely-ai-assistant/PRIVACY.md at main \- GitHub, [https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/blob/main/PRIVACY.md](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/blob/main/PRIVACY.md)  
19. Issues · Natively-AI-assistant/natively-cluely-ai-assistant \- GitHub, [https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/issues](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/issues)  
20. ai-assistant · GitHub Topics, [https://github.com/topics/ai-assistant?l=typescript\&o=desc\&s=stars](https://github.com/topics/ai-assistant?l=typescript&o=desc&s=stars)  
21. natively-cluely-ai-assistant Discussions\! \- GitHub, [https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/discussions](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant/discussions)  
22. iamsrikanthnani/pluely: The Open Source Alternative to Cluely \- A lightning-fast, privacy-first AI assistant that works seamlessly during meetings, interviews, and conversations without anyone knowing. Built with Tauri for native performance, just 10MB. Completely undetectable in video calls, screen shares, and recordings. · GitHub, [https://github.com/iamsrikanthnani/pluely](https://github.com/iamsrikanthnani/pluely)  
23. Compressa.ai \- GitHub, [https://github.com/compressa-ai](https://github.com/compressa-ai)  
24. I created an open-source alternative to Cluely called Pluely \- now at 600+ GitHub stars : r/SideProject \- Reddit, [https://www.reddit.com/r/SideProject/comments/1ncskfg/i\_created\_an\_opensource\_alternative\_to\_cluely/](https://www.reddit.com/r/SideProject/comments/1ncskfg/i_created_an_opensource_alternative_to_cluely/)  
25. I built a native Swift macOS AI client that's invisible to screen sharing — works with Ollama, vLLM, llama.cpp \[OC\] \- Reddit, [https://www.reddit.com/r/swift/comments/1tid7wq/i\_built\_a\_native\_swift\_macos\_ai\_client\_thats/](https://www.reddit.com/r/swift/comments/1tid7wq/i_built_a_native_swift_macos_ai_client_thats/)  
26. cluely · GitHub Topics, [https://github.com/topics/cluely?l=html\&o=asc\&s=stars](https://github.com/topics/cluely?l=html&o=asc&s=stars)  
27. OpenCluely is a free, open source Cluely (alternative), built for technical interviews like DSA, OAs, and CP. It offers an invisible overlay, real-time AI help, Smart Image Processing for question capture, and multi-language support : 100% customizable and private. · GitHub, [https://github.com/TechyCSR/OpenCluely](https://github.com/TechyCSR/OpenCluely)  
28. open-source-cluely · GitHub Topics, [https://github.com/topics/open-source-cluely](https://github.com/topics/open-source-cluely)  
29. Laxcorp-Research/project-raven: Open-source AI meeting copilot \- real-time transcription, echo cancellation, and AI assistance. Captures system audio \+ mic, cancels echo via WebRTC AEC3, transcribes with Deepgram, and gives you Claude/OpenAI help during meetings. Runs locally on macOS and Windows. · GitHub, [https://github.com/Laxcorp-Research/project-raven](https://github.com/Laxcorp-Research/project-raven)  
30. interview-copilot · GitHub Topics, [https://github.com/topics/interview-copilot?l=typescript](https://github.com/topics/interview-copilot?l=typescript)  
31. pikabaka/LICENSE at main · royisme/pikabaka · GitHub, [https://github.com/royisme/pikabaka/blob/main/LICENSE](https://github.com/royisme/pikabaka/blob/main/LICENSE)  
32. real-time-transcription · GitHub Topics · GitHub, [https://github.com/topics/real-time-transcription?l=typescript\&o=desc\&s=stars](https://github.com/topics/real-time-transcription?l=typescript&o=desc&s=stars)  
33. sqlite-vec · GitHub Topics, [https://github.com/topics/sqlite-vec?l=typescript](https://github.com/topics/sqlite-vec?l=typescript)  
34. Repowise \- GitHub, [https://github.com/repowise-dev](https://github.com/repowise-dev)  
35. GitHub \- tahahah/Clonely: a clone of Cluely, free and open-source., [https://github.com/tahahah/Clonely/](https://github.com/tahahah/Clonely/)  
36. SaimNadeemdev \- GitHub, [https://github.com/SaimNadeemdev](https://github.com/SaimNadeemdev)  
37. Releases · SaimNadeemdev/MindWhisperAI-Cluely-Free-Alternative \- GitHub, [https://github.com/SaimNadeemdev/MindWhisperAI-Cluely-Free-Alternative/releases](https://github.com/SaimNadeemdev/MindWhisperAI-Cluely-Free-Alternative/releases)  
38. GitHub \- varun-singhh/Vysper: Open Source Cluely: An AI-powered desktop tool that helps you excel in technical and professional interviews by providing intelligent, real-time assistance while remaining completely invisible to screen sharing and recording software., [https://github.com/varun-singhh/Vysper](https://github.com/varun-singhh/Vysper)  
39. Vysper/LICENSE at main · varun-singhh/Vysper · GitHub, [https://github.com/varun-singhh/Vysper/blob/main/LICENSE](https://github.com/varun-singhh/Vysper/blob/main/LICENSE)  
40. Vysper/package-lock.json at main · varun-singhh/Vysper · GitHub, [https://github.com/varun-singhh/Vysper/blob/main/package-lock.json](https://github.com/varun-singhh/Vysper/blob/main/package-lock.json)  
41. cluely · GitHub Topics, [https://github.com/topics/cluely](https://github.com/topics/cluely)  
42. Vexa — Open-Source Meeting Bot API | Self-Hosted Transcription, [https://vexa.ai/](https://vexa.ai/)  
43. Vexa-ai/vexa-lite-deploy \- GitHub, [https://github.com/Vexa-ai/vexa-lite-deploy](https://github.com/Vexa-ai/vexa-lite-deploy)  
44. Inulute \- Build Stuff That Makes Sense | Open Source Developer Tools, [https://inulute.com/](https://inulute.com/)  
45. Clonely/electron.vite.config.ts at master · tahahah/Clonely · GitHub, [https://github.com/tahahah/Clonely/blob/master/electron.vite.config.ts](https://github.com/tahahah/Clonely/blob/master/electron.vite.config.ts)  
46. Taha Ansari tahahah \- GitHub, [https://github.com/tahahah](https://github.com/tahahah)  
47. Activity · varun-singhh/Vysper \- GitHub, [https://github.com/varun-singhh/Vysper/activity](https://github.com/varun-singhh/Vysper/activity)  
48. \[App Request\]: Vexa with dashboard (open source, self-hosted fireflies.ai alternative) · Issue \#4333 \- GitHub, [https://github.com/truenas/apps/issues/4333](https://github.com/truenas/apps/issues/4333)  
49. ai-assistant · GitHub Topics, [https://github.com/topics/ai-assistant?l=swift](https://github.com/topics/ai-assistant?l=swift)  
50. Top Cluely Alternatives: Discover the Best AI Tool for Your Needs \- Bluedot, [https://www.bluedothq.com/blog/cluely-alternatives](https://www.bluedothq.com/blog/cluely-alternatives)  
51. Cluely Alternative | HuddleMate vs Cluely, [https://huddlemate.ai/cluely-ai-alternative](https://huddlemate.ai/cluely-ai-alternative)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAaCAYAAAAnkAWyAAABlklEQVR4Xu2WTSuEURTH/15SSGRDs7BTsvMhrCyUJIpm9hZs5EMoeyx9BNmwsLGklGJBlFISeaekOKdzb3PmzB2TmYdnJvdX/zovz9z5dzrd5wEikf/JBunzB6op2NBEoGaNDgRqqdINmbymEWLywNSZC1tIk01Sg6nNQ8yPmnoLadnUUmXOFog7hNeji9Rji7VGaN/rgiaI8T3bqAcWIeZHbCMhViDnt7mcb7CPfLs6nvD7K6PNt0MujUT4i33X5hODr8Lv9p37L5Ab6o2UcfVJyO8OXR4awBVpnXTqet68fbYX8i7h9b1W9bKsQQ7KmbqHr8lLF/sXmSeLvHlG9x5Jgyq3k9fP6riVdK/yIsZIr5C7/daJ9/4dxdNjeEdXSWco7E+htHl7Tinz0yr22LxiFiBT9OiDx0lHKi9nnoegc2ZGxR6bVwwflHVxn8t54sww6cTFjP7TZ9KQyrnXafJQ3E+6UXlVNJMeSLukWciH247q75O2UPiJ7TknbTv5XgdkRdkgXwQMrxPnx6QlV4tEIpEU+QJ5gnpmueFUOAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF4AAAAaCAYAAAA+G+sUAAADGUlEQVR4Xu2YS8hNURTHF0qJAVJeMWFgZGDklUfySlKSETKQAcJAnhmhKCkkr3DJYyClhAFhIBlI8iwlj5D3+/1e/9ZanXWW436+697Lp/2rf2ef/9p3n++svfc653xEiUQikfjfOcT63gglqgSSObHAi0nuVeAlKqQ9yYr3NCdJ8IXggzvRSFTGYVaz4M0lSfy44LdkrQleokLmRIN5TsUlpS2rYzQT1aOovidqTAuSpJ+LgURtWUCS+DEx0AQosU5HsxF8YI2KZr14TeXLzKpo/ENMYE2KZhlmhvN9rDbBqxsN1fdv0WiizKefE//XwOtiufpuk+Inx9rLWQ9ZI9X/zJrBesoaqF4nkr6PWUdZB1g3NAZ2slayDmo/4xRrD2s3azZrkcaXkbwO39N+/u/6qO1ZrGskO3mFxk5qzPe3Emt9wEbWVtYu1lL1NpH0w6RdZl0iKXF/BC6CQacG3+MTYsAbxhrN6qbe2yyc+033cP6F1VPb3n+nxxJrv7aHUlbDF5PUZIBJB10oPwZ252B3jlhfbSP5ccVvoSzxmDAk3DjCGqvt7ZTf+UU5aZDxJDeJd3esTgir4xMVD/i7Hr5+V7OuUj4ek4MJsmTcIonh78EXNcC57RjPQtbe4OE3fmys+j7u/CzriraLEr+OssRjnOEuhr62mDBBWPlG0f1XHbuIf+uJF+5Hv14R+ADz568oS3xrkq9olBPrg+MQbXuQ+FLw2lF+bOwIn/hjrIvaPkHZx2N/Pa6lfOLxsDbmkexOgBK03sXi/dcEu4ivhfHC51k7tG3fBZ31HKXI939D2Y3fd76VEdTW687HDgJLKF8KQFzxGAM72kAMkwvwzLC6PUiPfsVPZh3XNrjJGqHtbSTJN+L91wS8rqEsYQWA9yTlCd4U68TcZZ0hWUUlkuShzFhJQxl4oW14A0gelHjwPqD8cwYP06+s2yQTiaQ/U6Ekgg6UjW3/3EPip5NMFh72XdU3HmkMYAXbmLbSp5GMgdLXQ73Nrt8GkoXzhPVS4wmSSfGlJlEHepOUAOyOViGWSCQSiUTN+AFmquaH5/bfgAAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAaCAYAAAA5WTUBAAABQUlEQVR4Xu2VsWoCQRCGRwNp0mgwxkdI45NYCBFMSt9AIYWlrYVoGwiJEB9BfAjBwi5B0EJIZxIkJoWN/sOe3GRY74iuNrkPPriZWXaH3b07oogIO124+oMHgScuWnJ6wStLzgnnZHZCEiez2FDlmalOuKAHYypXIdNEXuVPYVPlnFDWCfBJ9m1PwEudPBS2+3BUTsg0MNCFY1Il00ROF8Az+Tt0Bl9F7JQvCp5Y1i5U7Iyw+yBrSRU7gV/BsPuwrYnN0WRhH77BO1iDHbjwxoXyQGaikspLtjXBTMgsvoFrGe/5HtZF7RfX8IfMt+Hdk+/FkuxbHdTECN6KWNZa8FHEexHUxAssiFjWGvBJxHshJ06reAxvRCxr/Llvi3hnvuEMzmGK/CPko+Nd4GfO8R+Zx/BYPlpu4MPTSSMREf+DNVYBYkSWfR60AAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABGCAYAAABxPchcAAAHWklEQVR4Xu3dd4gkSx0H8DI+cxafmFAxoIg5hz9VUDCAKIJ6IPqHijmnO1HBLAZMqJwoPjGLWVHMIk9UDKAY7sSEOedYX7uL6a3r2Z3dud23e/v5wI+rqe6aTrtXv6nq6S0FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADjcbl7jvyvGWWObg6w/pmXxudbgDNEf37J4TmvAruvP/bJwTQAoP6nx5snr85ehk/jGpC5Sd9Bdt8Y/a1x0Utc6xakTNR7f1R1kD63x0xrnm9TNHfd/atyiq2N3uCYAbEvfQTxqrLtnV9+vdxB9pcbFurocVzrFqRfWuFZXt59s91okSZ1qSfnXuvpzu9eszjUBYNfcssaDurrflPnOZ67uoOkTs8hxvbSr+2z3er/Z7rX4fvf60WV4j3t09f/uXrM61wSAPZVO47B0Em1U46BZd5/Tft33YKN1z6drAsC2pNN4UV95Hjuxjbji2GYVuU/tIHaS6+5z2h+WpHyvuCYA7Kl0HJfuK3dBvvn23b5yj/2hxpf7yjXdtwxTqk8bX19osux0WSc5uFXZn0n5nOv3FSu6TF+xB9a5JjF3TW5S45M13j2+/lgZPpQAcMjdumze8Vynr1hi1UdibLatvZDt362vPA2O13jBWM423r9YtC0XLkP7VWMVHy7DusuS8lf2Feeh7OcqCe+Lu9dp97iu7nTqz/tmcbWxzVaWXZOH1Pj8WM7v36rXGYAz2J/K8m+lfajGDfvKJVbtVFZdL8nPqnGpsc1WblNW3/52ZaSkJWy7YZ39bonEnJyTd/SVB8Cy49lL6+zDU8ry9vcqi4TtsmX5egAcIukM7t5XVn8tG0cNmh/VOFbjW+Pri5T59X5R4+E1fj2pi/Oy8/l4Wb79O9Z4X43nl8U+n102Hld/jHmW3afK8FiGd5YhYWsjlq3Djb/UeGKNX9a43KR+O5bt9yrSdm4a+Gg59dq18ifK8Ly+eEQZRrReX+MOY939xvWS0L+9DI+saMf2phrPq/HecZ1IYpjjf1YZPiS0hOXZNT5Yhm21n7mMsN12LD+mxhfLcK/Xfcpgus8/q/GksfzccXnaZxsZccu5v2CN14zr5GfymzX+Pq67jnZsO/HnMn9NYlnC1o45I6bvKsN7XL7GOWU4DwCcofLcsXQA+ebknNYhNz+sce3J6y9Nyn3n9a/x30fW+PSkvl9vL7UOb86xGs8cy9nn5hplY5tpOR1l85ayGGG7f1l0uDcupz4odSd22i7bTtsjXX1ztJw6wpb1L14WT9vPPVV3mSxrHliGBCiS8CaZj+k6SZjaNG/zj/Hfp9b421hu28p6bUo05f6Bx3PleF1ZJGz9svb6jWXxmJdnlI0Pj96Jfjur2uqaLEvYYlrO71h7htu3a9x1sgyAM0A6zN+VYSQpkU/q+c+/vw8tncM0Yes7qGUdSZOb8POMtx9M6ubW200ZmfljGfbjVzV+W4bRlbn9uEEZbvbOus2Vy/xx5nl2GTVqjpdFwnbvsuhwvzf+28xtdxXbbZfEJF+wyLHkGucc5Lr373O0zCdsvTuVYYp8uiyJaZPz0ZKvk2VYL8laRt1yXuZGtJ5c461dXdpNE7ap6YNn+2UvL1snbEnqMtIWT6jxkbG8U/12tjK9JvlZXHZNkrB9YSxvlrDl9/b2Y/mrNR4wWQbAIZIOJiNETd+xzHUkuYm6dTKZLs1064m20li/H2V0KNNMMZ0ivkKZP86MZrTpwThehr+WENMRkv5hqTs9/p2220pGFd9TNn4Ro99WkvlM6cZ0Wb4d29ysLBK2jM5lFCkjlVn/WFmMuE4lYTve1WX9ZQlbe/9oy9p+vaxsnbC9usYrxvJjy94nbKvKz0+mgWOzhC3JX/vQkOnVjHgCcAjlPqOXlMXUzY3K4r6mjKhcfSxHOpIjYzmPJmgdy8kyjK5kROF6Y/1+/DuJvy/DfVlJNE6W4VEYZ4/L2rF8fSxntGlaf8kyjORlJDEJa5KCTB9fZVyeKcU4UuNtY3m/SHKVkZ72d2STAOS4MsXZ5HWmws8ay0nU8hiN19a4cxmmLZ9ehgS/XfsL/L/lYgoyfyKsjUB+tMaVynDP4LllaBM3LUPbjFBGym3K72FluPesybJM5X+nDOf5MzU+UBbnP/cixqvK8Oy9q5YhCcoocsq55zCjn9Mp/v0g+59v7f64DN8QfXAZjjXnJklxK+eDVJLg3BOY36uf13hD2fk9kgAccElGekm40tFvpU3XzL3HfpQbuDMFGi3haNJZRjrKS0zqk+DkpvZMHW/2t0hzE33/ngfJNcvq38bN+ci57JOhJMNJLlbVEuK0yUhnbzpd38u2btdXAgBwerWEDQCAfSijs7k5P1PVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPvd/wDEZfrzUljF3gAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJIAAAAaCAYAAABcmAU7AAAEiElEQVR4Xu2Za8ilUxTHl+vkrkku4/K+HxDjA5J8GJLwAUUhIcyUIk1uZcykmC9TxkyUcgkhkVI+kHxwa8oll6hBjQ8jhJkwjPu4X9bP2ttZZ5193nefM2em87J/tTrP+q/n2c/lrGfvtfcj0mg0Go1Go9Hox1Nqfw1g/2e+UzsnisrBaq+LPZ/nQ8xzq9qval+pHR9imdq2xg4u+LyCFpPmsII207hR7B6OjYEKLhc7NibSiUnPHBX8zLdqy5z/k9py50NtW2PHbLEeybOt2MWvDjp8HIUZwr1qf4j9McOyQcqJhHZF0Oh1XnP+ydKbEDz7qNW0NZY8rbZN0K4Ru6Gzgr6j2m1BG3e4vx/U9o+BAfkm/cZE2jtp/HqeTXqGZIhJA2gXpe3atsaSq6OgfC3lC99TbZ8ojiHbifWm69V2C7FhuERtQdqOiXRT0iIPSrfO9m/Oz6C/k7Zr24qcrbZE7YHkz1K7Vm2p2g55J+V6sX2owSInqL0iVptR5qztDg8HFz3VhY8ru6qtU3tXLJlGBQV2JibSE0mL3Cm9ieTbyaBTK0FtW5HrxO6bfUiqK5N+c9Im1FYlLde5ZyYfVqo94vwLZerzVcEfQCNvxsAMgDriM7XdY2Az+Fy6h/6YSC8mLXK7mJ6HVLY3dsL/gp6Pr22rBL0M+zwWdLQ/C5q/FnwmEp7SdQzEYrFGzoiBEXGPWPs7J5835PdOeCQ8qfaj2gExMCCnq10VtJhIjyYtcoeYvn3y2c51lsf/0bVtlZgU22ci6Gh3FTR/nleT/5H0JtTQfC/lmxklPpF2ESuItwQ8QGZqR8ZAJXnI8cRE6lfX3C/dOtu/OD+DnuuR2rZK8NKwTyzU0VYUtNje+07HlnaHB6d0klFD+zmRtgY3iJ3ztBiYhpeCMdzTznvJh3lJi39gnGn1e65od6ft2rZKMOyxD0sKHrRbCppvbz+3zfFfyPTnmxKm9zTQrz4izpDBTI+3dU7Szxc7jiIX4oUCtcvD0sn8nEhx333F1qoYYrmhUcLsi3NdHAOVHCp2fGkdiSLXw5KDr0PoHeMzofZC8zOrmrZKTIodu1fQ0abrkeJ1AdrQE5b7xBpYEPQMU39mB5AXLTPzpZNI4GPMVuY6n5jvkfrd1E5Sris2l5PULo1iBbnHuCzo9Bi+zssJMuk0QDvC+W9I70yutq3IMWL7HR50tIcKWnzmzzg/awNB9m8SWzvi+w9GndRvAY2ahlXiD6Q7foH0T6TYDn4pkViYK+07DvB8eIk+Ufs0+Z63xXrrx8Wu+ZTu8D9MiMVeEOt180sZqWnL87PYmhnXxi+1GAU6o0C+Xj7PHCjWy2ftSw4WO8ep6Rfj3KwZbjEWSe+aSuZctTXOny6RSEjvA0NOad/Gfwz+1Plp+6Dk0xMBGe1XQ30CMMYf7XxiewS/tH2IdN6aGhiyWLaosViUNrYirGPQRb6stlDsM8QqF39LbIznIzAJ4ZPiQ7XnkuUYny8YRkkWulNgyMNnZrQyabXwQfa4ShvFp5NGo9FoNBqNRqPRaDRmAH8D4559RB3odEQAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABGCAYAAABxPchcAAAEoElEQVR4Xu3dS6h2UxgA4CV3kVu5JPzu1wEDUug3wUAZiELIn4FkYkAZSQiRa2FC/YkZAxnIrRQKuSQGyjX3+/1+X297b2ed9+zvOM7/qXP6nqfezlrv++3v7H1Gb2vvtU8pAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAs9NcS46nhgFXu6xpn19i+xoE17qlx0bxPlLJvjWdLd92Ppdrghhq/1viixjGpBgAwNfvX+K3Glk1uaNBab9e4OOVWq9yIvjS/XNb2+cFhNa5t5uGbGlc185+aMQDAVL1YY6uUi2blz5S7vsbeKbfS7JITE8T1XVPj9hobp1qI+gUjucXmO9R4JuUAAKYiN2axmhTNyE0p/2SarzRxzlfk5AS52cqivtNI7qx+HLWx7xjLAQBM3VdldTQesSr4Xo1XamySav8mrm/zGvfWuDHVwtj1R+6Dfry+xg9zpX+MHTeIWsTOpbsFGxHzeAYuziVuS7/Q5zbrjwlRi9y6Gg/144OaOgAwg4bGYiW7rsajOfkfxPU92I9j80HM26Zv7Prbv8vDpWtss6i3zwJmP5aFz7rFMbFpYbC2xpfNPBq645v5/UXDBgAzLxqI53Pyf7BFjUdqbJoLi7i7dCtRG9qwXJLmcc3fpnnWNmxx3pMatlhBmyRWBG9LuTgmdqvmXDv+uZmvqbFtMwcAZlA0CCflZG+pr/XYIycm2K8srWGLW4RxXnvlwpS0zdgwzyI3NGm31viuqQ3Gjmu9VeOMlBs7ps2d0M+HOLGpAQAz6Kgy3kAMFqu1Ps6JCWJlaSkNWytuCcatxeV6o3TXESt8g7GGbWzTwR39+Oh+no3lWq/XOCXlxo5pc7s243NLV3uiyQEAMyaeC/sjJ0vX3LSrPINo8J4r3e7MQ/tc7DodPnd+nzu2xgOla1gu7HNhOQ3bIB76vy8nl+DdsnDDQL6uGI81Vu255kZrozL/2bMx79Q4NeXy94R8Lq1bysLn4ACAGRLNwfqcbLTNQ+zSzI3F8E6z3GRcXuOyftzWNqRhC9vU+LAs/VZt2L3Gm838uNKd0wFNLp5R+72ZRzPWPuMW4phDmnk0rmua+ZjPyvj73dq/wdZ9bhDj2OQwiJ2iVzZzAGAGxIpaPI8Vq0Ofl64x+aUsbLpCm7uzxtPNPJqRS/vx2LEHl+4lvblha19hsVzRKMb3npcLE5xTus/Hazri59gLgV8uc6t4Y9ezZ+nyj5du1W545ccksRP0/dJ9Lr73tBqflG4jwkelaxJfK10DGrlPaxxRut8Ru0TjZ0S88BcAYKKhcYldinfVeLWpfV/j6n48fO7m/mc0IPHsWVsL0bDFe8ampV3xAgCYSXmlKVaGhmfX2v/HGbfwTi5zK17xfzdP73PR2B1ZY7e+fmbpbjkCADAl+6T5djUOT7kQDVlrx2Y89v87AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZsvfn0oBjpM4iRIAAAAASUVORK5CYII=>