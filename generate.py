import sys

import anyio
import dagger

ASCIIDOCTOR_IMAGE = "asciidoctor/docker-asciidoctor"
SRC_DIR = "./src"
BUILD_DIR = "./build"
RESUME = "README.adoc"


async def docs():
    config = dagger.Config(log_output=sys.stderr)

    async with dagger.Connection(config) as client:
        project = client.host().directory(".")

        build_dir = (
            client.container()
            .from_(ASCIIDOCTOR_IMAGE)
            .with_directory(SRC_DIR, project)
            .with_workdir(SRC_DIR)
            .with_exec(["mkdir", "-p", BUILD_DIR])
            .with_exec(
                [
                    "asciidoctor",
                    "-r",
                    "asciidoctor-pdf",
                    "-b",
                    "pdf",
                    "-r",
                    "asciidoctor-diagram",
                    "-D",
                    BUILD_DIR,
                    "-o",
                    "joshua.reynolds.resume.pdf",
                    RESUME,
                ]
            )
            .directory(BUILD_DIR)
        )

        await build_dir.export(BUILD_DIR)

        e = await build_dir.entries()

        print(e)


anyio.run(docs)
