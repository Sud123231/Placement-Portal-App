import csv
import os
from datetime import date, datetime, timedelta
from io import StringIO

from flask import current_app
from flask_mail import Message

from extensions import celery, mail
from models import Admin, Application, Placement_Drive, Student


def get_app():
    from app import app

    return app


def get_mail_sender():
    return current_app.config.get("MAIL_USERNAME")


def get_previous_month_range():
    """Return the first and last date of the previous calendar month."""
    today = date.today()

    if today.month == 1:
        report_month = 12
        report_year = today.year - 1
    else:
        report_month = today.month - 1
        report_year = today.year

    start_date = date(report_year, report_month, 1)
    if report_month == 12:
        end_date = date(report_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(report_year, report_month + 1, 1) - timedelta(days=1)

    return report_year, report_month, start_date, end_date


@celery.task
def send_daily_reminders():
    """Queue reminder emails for students with nearby eligible deadlines."""
    try:
        with get_app().app_context():
            students = Student.query.filter_by(status="Active").all()
            today = datetime.now().date()
            deadline_range_end = today + timedelta(days=7)

            upcoming_drives = Placement_Drive.query.filter(
                Placement_Drive.status == "Ongoing",
                Placement_Drive.application_deadline >= today,
                Placement_Drive.application_deadline <= deadline_range_end,
            ).all()

            for student in students:
                eligible_drives = []
                for drive in upcoming_drives:
                    already_applied = Application.query.filter_by(
                        student_id=student.student_id,
                        drive_id=drive.drive_id,
                    ).first()
                    if student.cgpa >= drive.min_cgpa and not already_applied:
                        eligible_drives.append(drive)
                    
                if eligible_drives:
                    send_reminder_email.delay(
                        student_email=student.user.email if student.user else None,
                        student_name=student.name,
                        drives=[
                            {
                                "title": drive.job_title,
                                "company": drive.company.name,
                                "deadline": str(drive.application_deadline),
                            }
                            for drive in eligible_drives
                        ],
                    )

        return {"status": "success", "message": "Daily reminders sent"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@celery.task
def send_reminder_email(student_email, student_name, drives):
    """Send an email reminder to a student about upcoming drives."""
    try:
        if not student_email:
            return {"status": "skipped", "message": "No email address"}

        with get_app().app_context():
            body_lines = [
                f"Dear {student_name},",
                "",
                "You have the following upcoming placement drives with approaching deadlines:",
                "",
            ]
            for drive in drives:
                body_lines.extend(
                    [
                        f"Drive: {drive['title']}",
                        f"Company: {drive['company']}",
                        f"Deadline: {drive['deadline']}",
                        "",
                    ]
                )
            body_lines.extend(
                [
                    "Please apply soon on the student dashboard to avoid missing the deadline!",
                    "",
                    "Best regards,",
                    "Placement Portal Team",
                ]
            )

            msg = Message(
                subject="Reminder: Upcoming Placement Drive Deadlines",
                recipients=[student_email],
                sender=get_mail_sender(),
                body="\n".join(body_lines),
            )
            mail.send(msg)
            return {"status": "success", "message": f"Email sent to {student_email}"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@celery.task
def send_monthly_activity_report():
    """Generate the previous month's summary and queue it for the admin."""
    try:
        with get_app().app_context():
            report_year, report_month, start_date, end_date = get_previous_month_range()

            drives_count = Placement_Drive.query.filter(
                Placement_Drive.application_deadline >= start_date,
                Placement_Drive.application_deadline <= end_date,
            ).count()
            applications_count = Application.query.filter(
                Application.application_date >= start_date,
                Application.application_date <= end_date,
            ).count()
            selected_count = Application.query.filter(
                Application.application_date >= start_date,
                Application.application_date <= end_date,
                Application.status == "Selected",
            ).count()

            admin = Admin.query.first()
            admin_email = admin.user.email if admin and admin.user else None
            if admin_email:
                send_monthly_report_email.delay(
                    admin_email=admin_email,
                    month=report_month,
                    year=report_year,
                    drives_count=drives_count,
                    applications_count=applications_count,
                    selected_count=selected_count,
                )

        return {"status": "success", "message": "Monthly report sent"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@celery.task
def send_monthly_report_email(admin_email, month, year, drives_count, applications_count, selected_count):
    """Send the monthly activity report email to the admin."""
    try:
        with get_app().app_context():
            month_name = datetime(year, month, 1).strftime("%B")
            selection_rate = round((selected_count / applications_count * 100) if applications_count else 0, 2)

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Monthly Placement Activity Report</h2>
                <p><strong>Period:</strong> {month_name} {year}</p>
                <h3>Key Metrics</h3>
                <ul>
                    <li><strong>Number of Placement Drives:</strong> {drives_count}</li>
                    <li><strong>Total Applications Received:</strong> {applications_count}</li>
                    <li><strong>Students Selected:</strong> {selected_count}</li>
                    <li><strong>Selection Rate:</strong> {selection_rate}%</li>
                </ul>
                <p>For detailed information, please log in to the Placement Portal.</p>
                <br>
                <p>Best regards,<br>Placement Portal System</p>
            </body>
            </html>
            """

            msg = Message(
                subject=f"Monthly Placement Activity Report - {month_name} {year}",
                recipients=[admin_email],
                sender=get_mail_sender(),
                html=body,
            )
            mail.send(msg)
            return {"status": "success", "message": f"Report sent to {admin_email}"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@celery.task
def export_student_applications_csv(student_id):
    """Export a student's applications to CSV and notify them when ready."""
    try:
        with get_app().app_context():
            student = Student.query.filter_by(student_id=student_id).first()
            if not student:
                return {"status": "error", "message": "Student not found"}

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(
                [
                    "Student ID",
                    "Student Name",
                    "Company Name",
                    "Drive Title",
                    "Application Date",
                    "Application Status",
                    "Salary (INR)",
                    "Location",
                    "Remarks"
                ]
            )

            applications = Application.query.filter_by(student_id=student_id).all()
            for application in applications:
                writer.writerow(
                    [
                        student.student_id,
                        student.name,
                        application.placement_drive.company.name,
                        application.placement_drive.job_title,
                        application.application_date.strftime("%d/%m/%Y"),
                        application.status,
                        application.placement_drive.salary or "N/A",
                        application.placement_drive.location,
                        application.remark or ""
                    ]
                )

            os.makedirs("uploads/exports", exist_ok=True)
            filename = f"student_{student_id}_applications_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join("uploads/exports", filename)
            with open(filepath, "w", newline="") as file:
                file.write(output.getvalue())

            if student.user and student.user.email:
                send_export_notification.delay(
                    student_email=student.user.email,
                    student_name=student.name,
                    filename=filename,
                )

            return {
                "status": "success",
                "message": "Export completed",
                "filename": filename,
                "filepath": filepath
            }
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@celery.task
def send_export_notification(student_email, student_name, filename):
    """Send an email when a student's export file is ready."""
    try:
        with get_app().app_context():
            msg = Message(
                subject="Your Application Export is Ready",
                recipients=[student_email],
                sender=get_mail_sender(),
                body=(
                    f"Dear {student_name},\n\n"
                    "Your placement application history has been successfully exported to CSV format.\n\n"
                    f"File: {filename}\n\n"
                    "You can download it from your dashboard.\n\n"
                    "Best regards,\n"
                    "Placement Portal Team"
                ),
            )
            mail.send(msg)
            return {"status": "success", "message": f"Notification sent to {student_email}"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}
