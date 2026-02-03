#!/usr/bin/env node    // tells OS to run this file using node
const fs = require('fs/promises'); // read + write files asynchronously | promises-based API

const path = require('path'); // safely handles path across various OSes

// remove node and script path
const args = process.argv.slice(2);

// flags specify what to do
const flags = {
  lines: args.includes('--lines'),
  chars: args.includes('--chars'),
  words: args.includes('--words'),
  unique: args.includes('--unique')
};

// files tell us where to do it
const files = args.filter(arg => !arg.startsWith('--'));

// Check if no file provided
if (files.length === 0) {
  console.error('No input files provided.');
  process.exit(1);
}

async function processFile(file, flags) {
  // Starts high-precision timer
  const startTime = process.hrtime.bigint();

  // Reads file contents
  const content = await fs.readFile(file, 'utf8');

  // Result object
  const result = {
    file
  };

  // Count characters
  if (flags.chars) {
    result.characters = content.length;
  }

  // Count lines
  if (flags.lines) {
    result.lines = content.split('\n').length;
  }

  // Count words
  if (flags.words) {
    const wordsArray = content.trim().split(/\s+/);
    result.words = content.trim() === '' ? 0 : wordsArray.length;
  }
    const endTime = process.hrtime.bigint();

  // Measure memory
  const memoryUsed = process.memoryUsage().rss;

  // Performance stats - In milliseconds
  result.executionTimeMs =
    Number(endTime - startTime) / 1_000_000;

  result.memoryMB =
    +(memoryUsed / 1024 / 1024).toFixed(2);

  return { result, content };
}

async function run() {
  try {
    // Process all files IN PARALLEL
    const results = await Promise.all(
      files.map(file => processFile(file, flags))
    );

    // Print results to console
    results.forEach(r => {
      console.log(r.result);
    });

    await fs.mkdir('logs', { recursive: true });

    const logFile = path.join(
      'logs',
      `performance-${Date.now()}.json`
    );

    await fs.writeFile(
      logFile,
      JSON.stringify(results.map(r => r.result), null, 2)
    );

    if (flags.unique) {
      await fs.mkdir('output', { recursive: true });

      await Promise.all(
        results.map(({ result, content }) => {
          const lines = content.split('\n');
          const uniqueLines = [...new Set(lines)];

          const outputFile = path.join(
            'output',
            `unique-${path.basename(result.file)}`
          );

          return fs.writeFile(
            outputFile,
            uniqueLines.join('\n')
          );
        })
      );
    }

  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Run the program
run();