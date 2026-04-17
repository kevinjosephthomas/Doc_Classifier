#!/bin/bash

# Argo CD Installation and Setup Script
# This script installs Argo CD and configures it to monitor your GitHub repository

echo "🚀 Installing Argo CD..."

# Install Argo CD using kubectl
kubectl apply -f k8s/argocd/install.yaml

echo "⏳ Waiting for Argo CD pods to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-application-controller -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-repo-server -n argocd

echo "🔑 Getting Argo CD admin password..."
ARGOCD_PASSWORD=$(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d)
echo "Argo CD Admin Password: $ARGOCD_PASSWORD"

# Get Argo CD server URL
ARGOCD_URL=$(kubectl get svc argocd-server -n argocd -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
if [ -z "$ARGOCD_URL" ]; then
    ARGOCD_URL="localhost:8080"
    echo "🌐 Port forward Argo CD UI: kubectl port-forward svc/argocd-server -n argocd 8080:443"
fi

echo "🎯 Argo CD UI: https://$ARGOCD_URL"
echo "👤 Username: admin"
echo "🔒 Password: $ARGOCD_PASSWORD"

echo "📦 Creating Argo CD Application..."
kubectl apply -f k8s/argocd/doc-classifier-app.yaml

echo "✅ Argo CD setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Access Argo CD UI at: https://$ARGOCD_URL"
echo "2. Login with admin / $ARGOCD_PASSWORD"
echo "3. The application 'doc-classifier-app' should appear and sync automatically"
echo "4. Monitor your deployments in the Argo CD dashboard"
echo ""
echo "🔄 GitOps Flow:"
echo "- Push changes to k8s/ folder in GitHub"
echo "- Argo CD detects changes and syncs automatically"
echo "- Your cluster state stays in sync with Git!"