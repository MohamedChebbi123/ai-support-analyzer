from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from connection.database import get_db
from models.data import Data
from models.classifieddata import ClassifiedDataByPriority

from transformers import pipeline

router = APIRouter()

# Initialize classifier once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

priority_labels = ["urgent", "low", "medium"]
software_issues = [
    # Core Functionality Failures
    "feature_crash_on_launch",
    "module_not_initializing",
    "critical_process_hang",
    "service_not_starting",
    "background_task_frozen",
    "command_not_executing",
    "transaction_rollback_fail",
    
    # UI-Specific Defects
    "ui_elements_overlapping",
    "text_cutoff_rendering",
    "modal_dialog_stuck",
    "dropdown_not_closing",
    "checkbox_state_not_saving",
    "radio_button_misselection",
    "tooltip_not_disappearing",
    "hover_state_frozen",
    "scrollbar_disappeared",
    "responsive_layout_breakage",
    "touch_target_too_small",
    "keyboard_navigation_loop",
    "focus_indicator_missing",
    "animation_frame_drops",
    "dark_mode_flash_on_load",
    "high_contrast_mode_broken",
    
    # Feature-Specific Failures
    "search_returning_wrong_results",
    "filter_not_applying",
    "sort_order_reversing",
    "pagination_duplicate_items",
    "undo_action_corrupting_data",
    "redo_stack_cleared_prematurely",
    "bulk_operation_timeout",
    "preview_pane_not_updating",
    "wysiwyg_editor_format_loss",
    "rich_text_pasting_broken",
    "spellcheck_false_positives",
    "autocomplete_suggestions_wrong",
    "voice_command_misinterpretation",
    "gesture_recognition_failure",
    
    # Data Processing Issues
    "csv_import_encoding_error",
    "excel_date_conversion_bug",
    "json_parse_syntax_failure",
    "xml_entity_expansion_attack",
    "sql_injection_vulnerability",
    "data_truncation_silent_fail",
    "floating_point_calculation_error",
    "timezone_conversion_mistake",
    "currency_rounding_error",
    "unit_conversion_wrong",
    
    # System Integration Problems
    "clipboard_integration_broken",
    "print_dialog_not_appearing",
    "camera_access_denied",
    "microphone_permission_loop",
    "gps_location_stale",
    "bluetooth_pairing_failure",
    "biometric_auth_bypass",
    "notification_sound_missing",
    "deep_link_not_opening_app",
    
    # Performance Degradation
    "infinite_loading_spinner",
    "lazy_loading_stuck",
    "memory_overflow_crash",
    "gpu_texture_leak",
    "database_lock_contention",
    "main_thread_blocked",
    "event_loop_saturation",
    
    # Security Vulnerabilities
    "password_plaintext_logging",
    "session_token_not_rotating",
    "cors_policy_misconfigured",
    "content_security_policy_break",
    "mixed_content_warning",
    "certificate_pinning_failure",
    "brute_force_protection_missing",
    
    # Edge Cases
    "leap_year_calculation_bug",
    "time_drift_accumulation",
    "unicode_emoji_rendering",
    "right_to_left_layout_break",
    "screen_reader_announcement_missing",
    "colorblind_mode_not_working",
    "haptic_feedback_missing",
    
    # Enterprise-Specific
    "ldap_sync_failure",
    "saml_assertion_invalid",
    "kerberos_ticket_expired",
    "vpn_split_tunnel_broken",
    "single_sign_on_redirect_loop",
    "audit_log_not_recording",
    "compliance_rule_violation",
    
    # Mobile-Specific
    "screen_rotation_lock_fail",
    "back_button_override_broken",
    "status_bar_overlap",
    "keyboard_covering_input",
    "deep_sleep_wakeup_crash",
    "background_refresh_failing",
    "app_clip_not_launching",
    
    # AI/ML Features
    "recommendation_bias_detected",
    "training_data_leakage",
    "model_serving_timeout",
    "confidence_threshold_wrong",
    "false_positive_rate_high",
    "feedback_loop_not_learning"
]

def classify_problem_locally(problem_text: str) -> dict:
    priority_result = classifier(problem_text, priority_labels)
    priority = priority_result['labels'][0]

    type_result = classifier(problem_text, software_issues)
    problem_type = type_result['labels'][0]

    return {"priority": priority, "type": problem_type}

@router.post("/priorityclassified")
def classify_by_priority(db: Session = Depends(get_db)):
    unclassified_entries = db.query(Data).all()

    for entry in unclassified_entries:
        classification = classify_problem_locally(entry.problem)
        problem_priority = classification.get("priority", "Unknown")
        problem_type = classification.get("type", "Unknown")

        print(f"\nProblem: {entry.problem[:60]}")
        print(f"Priority prediction: {problem_priority}")
        print(f"Type prediction: {problem_type}")

        classified_entry = ClassifiedDataByPriority(
            name=entry.name,
            lastname=entry.lastname,
            country=entry.country,
            email=entry.email,
            phone_number=entry.phone_number,
            problem=entry.problem,
            submission_date=entry.submission_date,
            problem_priority=problem_priority,
            problem_type=problem_type,
        )
        db.add(classified_entry)

    db.commit()
    return {"message": "Data classified and saved successfully"}
