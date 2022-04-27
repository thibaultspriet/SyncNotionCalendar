from crontab import CronTab
import os


class InitCron:
    def __init__(self):
        self.minutes = "0"
        self.hours = "8-22"
        self.days = "*"
        self.month = "*"
        self.years = "*"

        self.cron = CronTab(user=True)

    def add_job(self):
        command = f"cd {os.getcwd()} && ./syncNotionCalendar.zsh"
        existing_jobs = list(self.cron.find_comment("SyncNotionCalendar cron job"))
        if len(existing_jobs) == 0:
            job = self.cron.new(
                comment="SyncNotionCalendar cron job",
                command=command
            )
        else:
            job = existing_jobs[0]
        job.setall(self.minutes, self.hours, self.days, self.month, self.years)
        job.enable()
        self.cron.write()


if __name__ == '__main__':
    InitCron().add_job()

