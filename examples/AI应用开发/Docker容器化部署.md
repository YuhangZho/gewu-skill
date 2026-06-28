---
title: Docker容器化部署
category: AI应用开发
status: 已完成
track: 快轨
importance: 3
prereqs: ["API服务与FastAPI"]
groups: ["部署与评估"]
goal_tags: ["求职", "工程"]
aliases: ["Docker", "容器化"]
tags: ["Docker", "容器", "部署", "环境一致"]
created: 2026-06-28
related: ["API服务与FastAPI", "AI应用作品集项目"]
sources: ["https://docs.docker.com/", "https://fastapi.tiangolo.com/deployment/docker/"]
viz: ""
viz_source: ""
viz_chart: ""
viz_reason: "工具操作型"
---

# Docker容器化部署

## 一句话定位
> 它属于AI应用开发，是用来解决〔用容器化方式交付 AI 应用〕的——解决环境一致性与云端部署问题。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能为 AI 应用写 Dockerfile、构建镜像、本地跑通、部署到云，并理解为什么容器化是部署标配。

**重点结论**（5 条）：
1. **Docker 解决"在我机器上能跑"问题**：把应用+依赖+环境打包成镜像， anywhere 一样跑。AI 应用依赖复杂（Python+torch+transformers+系统库），尤其需要。
2. **AI 应用 Dockerfile 要点**：基础镜像选 python:slim、分阶段构建减小镜像、requirements 锁版本、.dockerignore 排除大文件、CUDA 镜像跑 GPU。
3. **docker-compose 编排多服务**：AI 应用常是 API+向量库+前端，compose 一键起全栈。
4. **部署到云**：本地跑通→推镜像到 Registry→云服务器拉取运行；或用云容器服务（ECS/Cloud Run/Cloudflare）。
5. **生产要点**：日志挂载、健康检查、资源限制、重启策略、 secrets 管理（API key 不进镜像）。

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要）</summary>

**起点认知**：知道 Docker 是"轻量虚拟机"，但没为 AI 应用写过 Dockerfile。

**核心要点**：AI 应用依赖多（Python+模型库+系统依赖），Docker 把它打包成镜像解决环境一致。Dockerfile 要小（slim 基础镜像+分层缓存）、要安全（secrets 不进镜像）、要可观测（日志+健康检查）。

**类比**：Docker 像把整个厨房（应用+锅碗瓢盆+食谱）打包成集装箱，运到任何地方打开就能开火，不用担心那边没锅没炉子。

**应用例子**：
1. RAG 服务：FastAPI+Chroma+embedding 模型打包，compose 一键起。
2. 模型服务：torch+transformers+CUDA 镜像，部署到 GPU 云。
3. 作品集项目：Docker 化让面试官一键跑你的 demo。

</details>

## 📚 参考资料
<details>
<summary>📚 参考资料</summary>

- **Docker 官方文档**（官方，2026-06-28）https://docs.docker.com/
- **FastAPI Docker 部署**（官方，2026-06-28）https://fastapi.tiangolo.com/deployment/docker/

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Solomon Hykes · Docker 创始人
- **身份**：Docker Inc 创始人
- **与本概念的关系**：容器化的普及者，让容器从运维专属变开发者标配
- **核心洞见**：容器让应用和基础设施解耦，开发者不用管部署环境
- **代表作**：Docker
- **扩展阅读**：[Docker 官网](https://www.docker.com/)

### 2. FastAPI 官方 · 部署最佳实践
- **身份**：FastAPI 团队
- **与本概念的关系**：官方提供 AI 应用的 Docker 部署模板
- **核心洞见**：AI 应用 Dockerfile 要小+分层缓存+多阶段构建
- **代表作**：FastAPI 部署文档
- **扩展阅读**：[FastAPI Docker 部署](https://fastapi.tiangolo.com/deployment/docker/)

</details>

## 相关
[[API服务与FastAPI]] · [[AI应用作品集项目]]
