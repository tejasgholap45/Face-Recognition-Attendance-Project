"""
Attendance Manager Module
Handles attendance tracking and Excel file operations
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import os


class AttendanceManager:
    def __init__(self, attendance_dir: str = "attendance"):
        """
        Initialize the attendance manager
        
        Args:
            attendance_dir: Directory to store attendance Excel files
        """
        self.attendance_dir = Path(attendance_dir)
        self.attendance_dir.mkdir(parents=True, exist_ok=True)
        self.today_file = None
        self.update_today_file()
    
    def update_today_file(self):
        """Update the current day's attendance file path"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.today_file = self.attendance_dir / f"Attendance_{today}.xlsx"
    
    def get_attendance_file(self, date: Optional[str] = None) -> Path:
        """
        Get the attendance file path for a specific date
        
        Args:
            date: Date string in YYYY-MM-DD format (default: today)
        
        Returns:
            Path to the attendance file
        """
        if date is None:
            self.update_today_file()
            return self.today_file
        else:
            return self.attendance_dir / f"Attendance_{date}.xlsx"
    
    def mark_attendance(self, name: str) -> Dict[str, any]:
        """
        Mark attendance for a person
        
        Args:
            name: Person's name
        
        Returns:
            Dictionary with status and message:
            - success: True if attendance marked, False if already marked
            - message: Status message
            - time: Time of attendance (if successful)
        """
        self.update_today_file()
        
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        
        # Check if file exists and load existing data
        if self.today_file.exists():
            try:
                df = pd.read_excel(self.today_file)
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                df = pd.DataFrame(columns=['Name', 'Date', 'Time'])
        else:
            df = pd.DataFrame(columns=['Name', 'Date', 'Time'])
        
        # Check if person already marked attendance today
        if not df.empty and name in df['Name'].values:
            existing_time = df[df['Name'] == name]['Time'].iloc[0]
            return {
                'success': False,
                'message': f"Attendance already marked at {existing_time}",
                'time': existing_time
            }
        
        # Add new attendance record
        new_record = pd.DataFrame({
            'Name': [name],
            'Date': [current_date],
            'Time': [current_time]
        })
        
        df = pd.concat([df, new_record], ignore_index=True)
        
        # Save to Excel
        try:
            df.to_excel(self.today_file, index=False)
            return {
                'success': True,
                'message': f"Attendance marked successfully at {current_time}",
                'time': current_time
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error saving attendance: {e}",
                'time': None
            }
    
    def get_today_attendance(self) -> pd.DataFrame:
        """
        Get today's attendance records
        
        Returns:
            DataFrame with today's attendance
        """
        self.update_today_file()
        
        if self.today_file.exists():
            try:
                return pd.read_excel(self.today_file)
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                return pd.DataFrame(columns=['Name', 'Date', 'Time'])
        else:
            return pd.DataFrame(columns=['Name', 'Date', 'Time'])
    
    def get_attendance_by_date(self, date: str) -> pd.DataFrame:
        """
        Get attendance records for a specific date
        
        Args:
            date: Date string in YYYY-MM-DD format
        
        Returns:
            DataFrame with attendance records
        """
        file_path = self.get_attendance_file(date)
        
        if file_path.exists():
            try:
                return pd.read_excel(file_path)
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                return pd.DataFrame(columns=['Name', 'Date', 'Time'])
        else:
            return pd.DataFrame(columns=['Name', 'Date', 'Time'])
    
    def get_all_attendance_dates(self) -> List[str]:
        """
        Get list of all dates with attendance records
        
        Returns:
            List of date strings in YYYY-MM-DD format
        """
        dates = []
        for file_path in self.attendance_dir.glob("Attendance_*.xlsx"):
            # Extract date from filename
            date_str = file_path.stem.replace("Attendance_", "")
            dates.append(date_str)
        
        return sorted(dates, reverse=True)
    
    def get_attendance_summary(self, start_date: Optional[str] = None, 
                              end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get attendance summary for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: all dates)
            end_date: End date in YYYY-MM-DD format (default: all dates)
        
        Returns:
            DataFrame with attendance summary
        """
        all_dates = self.get_all_attendance_dates()
        
        if start_date:
            all_dates = [d for d in all_dates if d >= start_date]
        if end_date:
            all_dates = [d for d in all_dates if d <= end_date]
        
        all_records = []
        for date in all_dates:
            df = self.get_attendance_by_date(date)
            if not df.empty:
                all_records.append(df)
        
        if all_records:
            return pd.concat(all_records, ignore_index=True)
        else:
            return pd.DataFrame(columns=['Name', 'Date', 'Time'])
    
    def is_present_today(self, name: str) -> bool:
        """
        Check if a person has marked attendance today
        
        Args:
            name: Person's name
        
        Returns:
            True if present, False otherwise
        """
        df = self.get_today_attendance()
        return not df.empty and name in df['Name'].values
    
    def get_attendance_count(self, name: str, start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> int:
        """
        Get attendance count for a person in a date range
        
        Args:
            name: Person's name
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            Number of days present
        """
        df = self.get_attendance_summary(start_date, end_date)
        if df.empty:
            return 0
        return len(df[df['Name'] == name])
