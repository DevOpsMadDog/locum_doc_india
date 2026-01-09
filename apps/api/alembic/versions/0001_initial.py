"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2024-09-01 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role", sa.Enum("clinic_admin", "clinic_staff", "doctor", "admin", name="userrole"), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("hashed_auth", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "clinic_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lng", sa.Float(), nullable=False),
        sa.Column("city", sa.String(length=64), nullable=False),
        sa.Column("pan", sa.String(length=32), nullable=True),
        sa.Column("gst", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "doctor_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("specialty", sa.Enum("dentist_general", "endodontist", "anesthetist", name="specialty"), nullable=False),
        sa.Column("reg_no", sa.String(length=64), nullable=False),
        sa.Column("verification_status", sa.Enum("pending", "approved", "rejected", name="verificationstatus"), nullable=False),
        sa.Column("home_lat", sa.Float(), nullable=True),
        sa.Column("home_lng", sa.Float(), nullable=True),
        sa.Column("cancels_count", sa.Integer(), nullable=True),
        sa.Column("no_show_count", sa.Integer(), nullable=True),
        sa.Column("on_time_rate", sa.Float(), nullable=True),
        sa.Column("avg_rating", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "credentials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctor_profiles.id"), nullable=False),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("file_url", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "shifts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic_profiles.id"), nullable=False),
        sa.Column("specialty", sa.Enum("dentist_general", "endodontist", "anesthetist", name="specialty"), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("pay_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lng", sa.Float(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("auto_replace", sa.Boolean(), nullable=True),
        sa.Column("status", sa.Enum(
            "draft",
            "posted",
            "booked",
            "en_route",
            "checked_in",
            "completed",
            "paid",
            "canceled",
            "no_show",
            name="shiftstatus",
        ), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "shift_assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shift_id", sa.Integer(), sa.ForeignKey("shifts.id"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctor_profiles.id"), nullable=False),
        sa.Column("status", sa.Enum(
            "pending",
            "accepted",
            "canceled",
            "en_route",
            "checked_in",
            "completed",
            name="assignmentstatus",
        ), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), nullable=True),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "location_pings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assignment_id", sa.Integer(), sa.ForeignKey("shift_assignments.id"), nullable=False),
        sa.Column("ts", sa.DateTime(), nullable=True),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lng", sa.Float(), nullable=False),
        sa.Column("speed", sa.Float(), nullable=True),
        sa.Column("heading", sa.Float(), nullable=True),
        sa.Column("accuracy", sa.Float(), nullable=True),
    )
    op.create_table(
        "otp_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assignment_id", sa.Integer(), sa.ForeignKey("shift_assignments.id"), nullable=False),
        sa.Column("type", sa.Enum("checkin", "checkout", name="otptype"), nullable=False),
        sa.Column("otp_code", sa.String(length=8), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("used_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shift_id", sa.Integer(), sa.ForeignKey("shifts.id"), nullable=False),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic_profiles.id"), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("status", sa.Enum("created", "paid", "failed", name="paymentstatus"), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=True),
        sa.Column("provider_order_id", sa.String(length=128), nullable=True),
        sa.Column("provider_payment_id", sa.String(length=128), nullable=True),
    )
    op.create_table(
        "payouts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shift_id", sa.Integer(), sa.ForeignKey("shifts.id"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctor_profiles.id"), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("status", sa.Enum("pending", "paid", "failed", name="payoutstatus"), nullable=False),
        sa.Column("provider_payout_id", sa.String(length=128), nullable=True),
    )
    op.create_table(
        "ratings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shift_id", sa.Integer(), sa.ForeignKey("shifts.id"), nullable=False),
        sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic_profiles.id"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctor_profiles.id"), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
    )
    op.create_table(
        "shift_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shift_id", sa.Integer(), sa.ForeignKey("shifts.id"), nullable=False),
        sa.Column("assignment_id", sa.Integer(), sa.ForeignKey("shift_assignments.id"), nullable=True),
        sa.Column("event", sa.String(length=64), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("shift_events")
    op.drop_table("ratings")
    op.drop_table("payouts")
    op.drop_table("payments")
    op.drop_table("otp_sessions")
    op.drop_table("location_pings")
    op.drop_table("shift_assignments")
    op.drop_table("shifts")
    op.drop_table("credentials")
    op.drop_table("doctor_profiles")
    op.drop_table("clinic_profiles")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS payoutstatus")
    op.execute("DROP TYPE IF EXISTS paymentstatus")
    op.execute("DROP TYPE IF EXISTS otptype")
    op.execute("DROP TYPE IF EXISTS assignmentstatus")
    op.execute("DROP TYPE IF EXISTS shiftstatus")
    op.execute("DROP TYPE IF EXISTS verificationstatus")
    op.execute("DROP TYPE IF EXISTS specialty")
    op.execute("DROP TYPE IF EXISTS userrole")
