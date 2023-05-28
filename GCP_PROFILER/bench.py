import os
import googlecloudprofiler

VERSION_DEP = os.getenv('VERSION_DEP')

def main():
    # Profiler initialization. It starts a daemon thread which continuously
    # collects and uploads profiles. Best done as early as possible.
    try:
        googlecloudprofiler.start(
            service='fls_response',
            service_version=VERSION_DEP,
            # verbose is the logging level. 0-error, 1-warning, 2-info,
            # 3-debug. It defaults to 0 (error) if not set.
            verbose=3,
            # project_id must be set if not running on GCP.
            # project_id='my-project-id',
        )
    except (ValueError, NotImplementedError) as exc:
        print(exc)  # Handle errors here
# [END profiler_python_quickstart]
    busyloop()


# A loop function which spends 30% CPU time on loop3() and 70% CPU time
# on loop7().
def busyloop():
    while True:
        loop3()
        loop7()


def loop3():
    for _ in range(3):
        loop()


def loop7():
    for _ in range(7):
        loop()


def loop():
    for _ in range(10000):
        pass


if __name__ == '__main__':
    main()