# ASIC onboarding

Everything you need for the ASIC (Aggie Silicon & Integrated Circuits) onboarding rotation.

## Start here

Go through these in order:

1. [`setup/`](setup/README.md): install the tools on your computer
2. [`digital-design/`](digital-design/README.md): Block 1, build a traffic light controller
3. [`verification/`](verification/README.md): Block 2, write testbenches and find bugs
4. [`physical-design/`](physical-design/README.md): Block 3, turn your design into a chip layout

Each block's README links to its lessons. Do the lessons in order; each one ends with a
link to the next.

## What's in this repo

```
silicon-aggies-onboarding/
├── setup/
│   ├── README.md              install guide
│   └── check.sh               checks that every tool is installed
│
├── digital-design/            Block 1
│   ├── README.md              start here for Block 1
│   ├── lessons/               Lessons 0 to 4
│   ├── starter/               files you copy into your submission folder
│   ├── submission-template/   write-up template
│   ├── TROUBLESHOOTING.md
│   └── GLOSSARY.md
│
├── verification/              Block 2
│   ├── README.md              start here for Block 2
│   ├── lessons/               Lessons 0 to 5
│   ├── golden_counter/        working counter (Lesson 1)
│   ├── buggy_counter/         counter with bugs (Lesson 2)
│   ├── golden_counter_sram/   working counter-SRAM (Lesson 3)
│   ├── buggy_counter_sram/    counter-SRAM with bugs (Lesson 4)
│   ├── submission-template/   write-up template
│   ├── TROUBLESHOOTING.md
│   └── GLOSSARY.md
│
├── physical-design/           Block 3
│   ├── README.md              start here for Block 3
│   ├── lessons/               Lessons 0 to 6
│   ├── starter/               config.yaml for LibreLane
│   ├── submission-template/   write-up template
│   ├── TROUBLESHOOTING.md
│   └── GLOSSARY.md
│
├── submissions/               your work goes here
│   ├── digital-design/YOUR-GITHUB-USERNAME/
│   ├── verification/YOUR-GITHUB-USERNAME/
│   └── physical-design/YOUR-GITHUB-USERNAME/
│
└── SUBMITTING.md              how to turn in work, for every block
```

## Where to look

| If you... | Go to |
|---|---|
| haven't installed anything yet | [`setup/README.md`](setup/README.md) |
| got an error | the `TROUBLESHOOTING.md` in that block's folder |
| don't know what a word means | the `GLOSSARY.md` in that block's folder |
| are ready to turn in a block | [`SUBMITTING.md`](SUBMITTING.md) |
| are still stuck | the ASIC GroupMe, with the command you ran, the full error text, and your operating system |
