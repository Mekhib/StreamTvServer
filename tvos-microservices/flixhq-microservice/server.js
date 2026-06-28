
import { File, Blob } from 'node:buffer';
global.File = File;
global.Blob = Blob;

import express from 'express';
import { MOVIES } from 'flixhq-core';
import cors from 'cors';


const app = express();
app.use(cors());
const flixhq = new MOVIES.FlixHQ();

app.get('/search', async (req, res) => {
    try {
        const results = await flixhq.search(req.query.query);
        res.json({ results: results.results || results });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.get('/info', async (req, res) => {
    try {
        const info = await flixhq.fetchMovieInfo(req.query.mediaId);
        res.json(info);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.get('/sources', async (req, res) => {
    try {
        const { mediaId, episodeId } = req.query;
        const servers = await flixhq.fetchEpisodeServers(episodeId, mediaId);
        
        let allSources = [];
        for (const srv of servers) {
            try {
                const src = await flixhq.fetchEpisodeSources(episodeId, mediaId, srv.id);
                allSources.push({ server: srv.name, stream_data: src });
            } catch(err) {
                console.error("Failed to fetch source for server:", srv.name);
            }
        }
        res.json({ sources: allSources });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.listen(3000, () => console.log('FlixHQ Microservice on 3000'));
