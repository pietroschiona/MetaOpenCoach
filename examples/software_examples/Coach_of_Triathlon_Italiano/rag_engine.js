/**
 * RAG_ENGINE.JS - Vector Semantic Search Engine via API
 * Uses external LLM providers (OpenAI compatible, e.g. LM Studio/Ollama) via API /v1/embeddings.
 */

/**
 * Internal helper for HTTP POST compatible with pkg (no external libraries).
 */
function llmEmbedPost(url, body, headers, timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
        const parsed = new URL(url);
        const transport = parsed.protocol === 'https:' ? require('https') : require('http');
        const postData = JSON.stringify(body);
        let safeHostname = parsed.hostname;
        if (safeHostname === 'localhost') safeHostname = '127.0.0.1';

        const options = {
            hostname: safeHostname,
            port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
            path: parsed.pathname + (parsed.search || ''),
            method: 'POST',
            headers: { ...headers, 'Content-Length': Buffer.byteLength(postData) }
        };

        const req = transport.request(options, (res) => {
            let data = '';
            res.on('data', chunk => { data += chunk; });
            res.on('end', () => {
                try { resolve({ data: JSON.parse(data), status: res.statusCode }); }
                catch (e) { reject(new Error('JSON parse error on embeddings')); }
            });
        });

        req.on('error', reject);
        if (timeoutMs) req.setTimeout(timeoutMs, () => { req.destroy(); reject(new Error('timeout')); });
        req.write(postData);
        req.end();
    });
}

/**
 * Generates vector embedding for text by delegating to AI Provider.
 */
async function generateEmbedding(text, baseUrl, apiKey, modelName) {
    if (!text || text.trim() === '') return Array(384).fill(0.0001);
    
    // Normalize base URL by removing "/chat/completions" if user accidentally added it
    const safeBaseUrl = (baseUrl || 'https://api.openai.com/v1').replace(/(\/chat\/completions|\/completions)$/, '');
    const embeddingsUrl = `${safeBaseUrl}/embeddings`;
    
    try {
        const response = await llmEmbedPost(
            embeddingsUrl,
            { model: modelName || 'n/a', input: text.substring(0, 8000) }, // Safety token limit
            {
                'Authorization': `Bearer ${apiKey || 'no-auth'}`,
                'Content-Type': 'application/json'
            },
            5000 // 5 second timeout
        );
        
        if (response.data && response.data.data && response.data.data[0] && response.data.data[0].embedding) {
            return response.data.data[0].embedding;
        }
        throw new Error("Invalid embeddings response format");
    } catch (e) {
        console.warn(`[RAG WARN] Vector API error (${e.message}). Fallback degraded mode.`);
        return Array(384).fill(0.0001);
    }
}

/**
 * Calculates Cosine Similarity between two vectors.
 */
function cosineSimilarity(vecA, vecB) {
    if (!vecA || !vecB || vecA.length !== vecB.length) return 0;
    let dotProduct = 0, magnitudeA = 0, magnitudeB = 0;
    
    for (let i = 0; i < vecA.length; i++) {
        dotProduct += vecA[i] * vecB[i];
        magnitudeA += vecA[i] * vecA[i];
        magnitudeB += vecB[i] * vecB[i];
    }
    
    magnitudeA = Math.sqrt(magnitudeA);
    magnitudeB = Math.sqrt(magnitudeB);
    
    if (magnitudeA * magnitudeB === 0) return 0;
    return dotProduct / (magnitudeA * magnitudeB);
}

/**
 * Performs semantic search (Top K) on a list of documents.
 */
function getTopK(queryVector, documents, k = 3) {
    if (!queryVector || queryVector.length === 0) return [];
    
    const scoredDocs = documents
        .map(doc => ({
            ...doc,
            similarity: cosineSimilarity(queryVector, doc.embedding || [])
        }))
        .filter(doc => doc.embedding && doc.embedding.length > 0)
        .sort((a, b) => b.similarity - a.similarity);

    return scoredDocs.slice(0, k);
}

module.exports = {
    generateEmbedding,
    getTopK,
    cosineSimilarity
};
