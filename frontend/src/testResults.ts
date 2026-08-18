// take everything returned by FastAPI and store it in data 
// to run: npx tsx src/testResults.ts
async function testResults() {
  const response = await fetch("http://127.0.0.1:8000/backtest");
  const data = await response.json();

  console.log("Top-level fields:", Object.keys(data));

  for (const [name, value] of Object.entries(data)) {
    console.log(`\n--- ${name} ---`);

    if (Array.isArray(value) && value.length > 0) {
      console.log("Fields:");
      
      for (const field of Object.keys(value[0])) {
        console.log(`  - ${field}`);
      }

      console.log("\nExample object:");
      console.log(value[0]);
    } else {
      console.log(value);
    }
  }
}

testResults();