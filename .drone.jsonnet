local pipeline(python_version, os) = {
    local python_image = (
        (if os == "windows" then "winamd64/" else "") + "python:" + python_version
    ),

    kind: "pipeline",
    name: "python:" + python_version + "-" + os + ":amd64",

    platform: {
        os: os,
        arch: "amd64"
    },
    steps: [
        {
            name: "tests",
            image: python_image,
            commands: [
                "make requirements",
                "make tests"
            ]
        }
    ],
};

local python_versions = [
  "3.6",
  "3.7"
];

local platforms = [
  "linux",
  "windows"
];

[
    pipeline(python, platform)
    for python in python_versions
    for platform in platforms
]
