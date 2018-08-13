LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := dumptool
LOCAL_CFLAGS += -pie -fPIE
LOCAL_LDFLAGS += -pie -fPIE
LOCAL_SRC_FILES := dumptool.c  util.c 
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_CFLAGS += -pie -fPIE
LOCAL_LDFLAGS += -pie -fPIE
LOCAL_MODULE := dumpmem
LOCAL_SRC_FILES := dumpmem.c  util.c 
include $(BUILD_EXECUTABLE)
