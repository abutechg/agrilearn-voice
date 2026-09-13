$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Speech

$outputDir = Join-Path $PSScriptRoot "pipeline_fixture"
$audioDir = Join-Path $outputDir "audio"
New-Item -ItemType Directory -Force -Path $audioDir | Out-Null

$audioPath = Join-Path $audioDir "sample_0001.wav"
$text = "How do I prepare my soil before planting maize?"
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.SetOutputToWaveFile($audioPath)
$synthesizer.Speak($text)
$synthesizer.Dispose()

$manifest = @(
    [ordered]@{
        id = "fixture-0001"
        audio = "benchmark/pipeline_fixture/audio/sample_0001.wav"
        reference = $text
        languagePair = "English"
        topic = "Soil preparation"
        synthetic = $true
    }
)
$manifest | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $outputDir "manifest.json") -Encoding UTF8
Write-Host "Created synthetic pipeline fixture: $audioPath"